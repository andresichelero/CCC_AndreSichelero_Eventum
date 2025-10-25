from logging import warning
from datetime import datetime, timezone
from flask import (
    url_for,
    redirect,
    jsonify,
    flash,
    g,
    abort,
    Response,
    send_from_directory,
    request,
)
from flask_mail import Message
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm, mail
from werkzeug.utils import secure_filename
import os
import magic
import pyclamd
from app.forms import (
    SubmissionEvalForm,
    SubmissionForm,
    allowed_file,
)
import time
import io
import csv
from threading import Thread
from app.models import Activity, Submission, User, Event


# --- Função Helper para Envio de E-mail ---
def send_email(subject, recipients, text_body, html_body):
    """Função auxiliar para enviar e-mails assíncrona."""
    sender = app.config.get("MAIL_DEFAULT_SENDER")
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body

    # Obtém o contexto da aplicação atual
    app_context = app.app_context()

    # Inicia uma thread separada para enviar o e-mail
    # Isso impede que o request do usuário (ex: /register)
    # fique travado esperando o servidor SMTP.
    thr = Thread(target=_send_async_email, args=[app_context, msg])
    thr.start()


def _send_async_email(app_context, msg):
    """
    Função interna para envio em background (em uma thread).
    Tenta enviar, espera 60s em caso de falha, e tenta novamente.
    """
    # Precisamos do contexto da aplicação para acessar 'mail' e a configuração
    with app_context:
        try:
            mail.send(msg)
        except Exception as e:
            warning(f"Erro ao enviar e-mail (Tentativa 1): {e}")
            warning("Tentando novamente em 60 segundos...")
            time.sleep(60)  # Pausa por 1 minuto
            try:
                mail.send(msg)
                warning("E-mail enviado na Tentativa 2.")
            except Exception as e2:
                warning(f"Erro ao enviar e-mail (Tentativa 2): {e2}")
                warning("Desistindo do envio.")
                # Em produção, logaríamos isso de forma mais robusta


# Carrega o utilizador para o Flask-Login
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


# Define o utilizador global 'g.user' antes de cada request
@app.before_request
def before_request():
    g.user = current_user


# --- Rotas Principais ---
@app.route("/api/events")
def list_events():
    """Página para listar todos os eventos PÚBLICOS."""
    # Filtra os eventos para mostrar apenas os com status=2 (Publicado)
    events = Event.query.filter_by(status=2).order_by(Event.start_date.desc()).all()
    return jsonify({"events": [event.to_dict() for event in events]})


@app.route("/api/")
def index():
    # --- Lógica do Dashboard ---
    if g.user is not None and g.user.is_authenticated:
        # Coleta dados relevantes para o dashboard

        # Eventos que o usuário está inscrito
        # (lazy='subquery' no modelo, então a lista já está carregada)
        inscribed_events = g.user.inscribed_events

        # Submissões do usuário
        # (lazy='dynamic' no modelo, precisamos executar a query)
        submissions = g.user.submissions.order_by(Submission.id.desc()).all()

        # Eventos que o usuário organiza
        # (lazy='dynamic' no modelo, precisamos executar a query)
        organized_events = g.user.organized_events.order_by(
            Event.start_date.desc()
        ).all()

        # Eventos públicos futuros (para participantes)
        upcoming_events = (
            Event.query.filter(
                Event.status == 2,  # Publicado
                Event.start_date
                >= datetime.now(
                    timezone.utc
                ),  # TODO: Implementar lógica para eventos acontecendo agora
            )
            .order_by(Event.start_date.asc())
            .limit(5)
            .all()
        )

        return jsonify(
            {
                "authenticated": True,
                "user": {
                    "id": g.user.id,
                    "name": g.user.name,
                    "email": g.user.email,
                    "role": g.user.role,
                },
                "data": {
                    "inscribed_events": [e.to_dict() for e in inscribed_events],
                    "submissions": [s.to_dict() for s in submissions],
                    "organized_events": [e.to_dict() for e in organized_events],
                    "upcoming_events": [e.to_dict() for e in upcoming_events],
                },
            }
        )

    # Se não estiver logado, mostra a página de índice padrão
    return jsonify({"authenticated": False})


# --- Autenticação ---
@app.route("/api/register", methods=["POST"])
def register():
    if g.user is not None and g.user.is_authenticated:
        return jsonify({"success": True, "message": "Usuário já está logado!"})

    data = request.get_json()
    if (
        not data
        or "name" not in data
        or "email" not in data
        or "password" not in data
        or "role" not in data
    ):
        return jsonify({"error": "Name, email, password, and role required."}), 400

    # --- Verifica se o e-mail já existe ---
    existing_user = User.query.filter_by(email=data["email"]).first()
    if existing_user:
        return (
            jsonify(
                {
                    "error": "Este email já está registrado. Faça login ou use outro endereço."
                }
            ),
            409,
        )

    # --- Cria novo usuário ---
    user = User(name=data["name"], email=data["email"], role=int(data["role"]))
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()

    # --- Enviar E-mail de Confirmação de Registro ---
    send_email(
        subject="Bem-vindo(a) ao Eventum!",
        recipients=[user.email],
        text_body=f"Olá {user.name},\n\nSeu registro na plataforma Eventum foi realizado com sucesso.",
        html_body=f"<p>Olá {user.name},</p><p>Seu registro na plataforma Eventum foi realizado com sucesso.</p>",
    )

    return jsonify(
        {
            "success": True,
            "message": "Registro realizado com sucesso! Faça login para continuar.",
        }
    )


@app.route("/api/login", methods=["POST"])
def login():
    if g.user is not None and g.user.is_authenticated:
        return jsonify({"success": True, "message": "Usuário já está logado!"})

    data = request.get_json()
    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Email and password required."}), 400

    user = User.query.filter_by(email=data["email"]).first()
    if user is None or not user.check_password(data["password"]):
        return jsonify({"error": "Email ou senha inválidos."}), 401

    login_user(user)
    return jsonify({"success": True, "message": "Login realizado com sucesso!"})


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/api/logout", methods=["POST"])
@login_required
def api_logout():
    logout_user()
    return jsonify({"success": True, "message": "Logout realizado com sucesso!"})


# --- Gestão de Eventos (Apenas para Organizadores) ---
@app.route("/api/events", methods=["POST"])
@login_required
def create_event():
    # Proteção de Rota: Apenas utilizadores com role=1 (Organizador) podem usar esta rota
    if g.user.role != 1:
        return (
            jsonify(
                {
                    "error": "Acesso não autorizado. Apenas organizadores podem criar eventos."
                }
            ),
            403,
        )

    data = request.get_json()
    if not data:
        return jsonify({"error": "Dados JSON obrigatórios."}), 400

    required_fields = [
        "title",
        "description",
        "start_date",
        "end_date",
        "inscription_start_date",
        "inscription_end_date",
        "status",
    ]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Campo obrigatório: {field}"}), 400

    try:
        event = Event(
            title=data["title"],
            description=data["description"],
            start_date=datetime.fromisoformat(data["start_date"]),
            end_date=datetime.fromisoformat(data["end_date"]),
            inscription_start_date=datetime.fromisoformat(
                data["inscription_start_date"]
            ),
            inscription_end_date=datetime.fromisoformat(data["inscription_end_date"]),
            submission_start_date=(
                datetime.fromisoformat(data["submission_start_date"])
                if data.get("submission_start_date")
                else None
            ),
            submission_end_date=(
                datetime.fromisoformat(data["submission_end_date"])
                if data.get("submission_end_date")
                else None
            ),
            status=int(data["status"]),
            organizer_id=g.user.id,  # Associa o evento ao utilizador logado
        )
        db.session.add(event)
        db.session.commit()
        return (
            jsonify(
                {
                    "success": True,
                    "message": "Evento criado com sucesso!",
                    "event": event.to_dict(),
                }
            ),
            201,
        )
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro ao criar evento.", "details": str(e)}), 500


@app.route("/api/my-organized-events")
@login_required
def my_organized_events():
    """Retorna a lista de eventos (incluindo rascunhos) do organizador logado."""

    # Proteção de Rota: Apenas utilizadores com role=1 (Organizador)
    if g.user.role != 1:
        return (
            jsonify(
                {
                    "error": "Acesso não autorizado. Apenas organizadores podem ver eventos organizados."
                }
            ),
            403,
        )

    # Busca todos os eventos onde o organizer_id é o do usuário logado
    events = (
        Event.query.filter_by(organizer_id=g.user.id)
        .order_by(Event.start_date.desc())
        .all()
    )

    return jsonify({"events": [event.to_dict() for event in events]})


@app.route("/api/events/<int:event_id>")
def view_event(event_id):
    """Retorna os detalhes de um evento específico."""
    event = Event.query.get_or_404(event_id)
    activities = event.activities.order_by(Activity.start_time).all()
    # Lógica para verificar se as inscrições estão abertas
    now = datetime.now(timezone.utc)
    # Converte as datas do DB (naive) para aware (assumindo que são UTC)
    start_date = event.inscription_start_date.replace(tzinfo=timezone.utc)
    end_date = event.inscription_end_date.replace(tzinfo=timezone.utc)
    is_inscription_open = event.status == 2 and start_date <= now <= end_date

    is_submission_open = False
    if event.submission_start_date and event.submission_end_date:
        sub_start_date = event.submission_start_date.replace(tzinfo=timezone.utc)
        sub_end_date = event.submission_end_date.replace(tzinfo=timezone.utc)
        is_submission_open = event.status == 2 and sub_start_date <= now <= sub_end_date

    event_dict = event.to_dict()
    event_dict["organizer"] = event.organizer.to_dict()
    event_dict["participants"] = [p.to_dict() for p in event.participants]
    if g.user and event.organizer_id == g.user.id:
        event_dict["submissions"] = [s.to_dict() for s in event.submissions.all()]

    return jsonify(
        {
            "event": event_dict,
            "activities": [activity.to_dict() for activity in activities],
            "is_inscription_open": is_inscription_open,
            "is_submission_open": is_submission_open,
        }
    )


@app.route("/event/edit/<int:event_id>", methods=["GET", "POST"])
@login_required
def edit_event(event_id):
    """Permite que o organizador edite um evento."""
    event = Event.query.get_or_404(event_id)

    # Verifica se o usuário logado é o organizador do evento
    if event.organizer_id != g.user.id:
        return (
            jsonify(
                {
                    "error": "Acesso não autorizado. Você não é o organizador deste evento."
                }
            ),
            403,
        )

    data = request.get_json()
    if not data:
        return jsonify({"error": "Dados JSON obrigatórios."}), 400

    try:
        if "title" in data:
            event.title = data["title"]
        if "description" in data:
            event.description = data["description"]
        if "start_date" in data:
            event.start_date = datetime.fromisoformat(data["start_date"])
        if "end_date" in data:
            event.end_date = datetime.fromisoformat(data["end_date"])
        if "inscription_start_date" in data:
            event.inscription_start_date = datetime.fromisoformat(
                data["inscription_start_date"]
            )
        if "inscription_end_date" in data:
            event.inscription_end_date = datetime.fromisoformat(
                data["inscription_end_date"]
            )
        if "submission_start_date" in data:
            event.submission_start_date = (
                datetime.fromisoformat(data["submission_start_date"])
                if data["submission_start_date"]
                else None
            )
        if "submission_end_date" in data:
            event.submission_end_date = (
                datetime.fromisoformat(data["submission_end_date"])
                if data["submission_end_date"]
                else None
            )
        if "status" in data:
            event.status = int(data["status"])

        db.session.commit()
        return jsonify(
            {
                "success": True,
                "message": "Evento atualizado com sucesso!",
                "event": event.to_dict(),
            }
        )
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro ao atualizar evento.", "details": str(e)}), 500


@app.route("/api/events/<int:event_id>", methods=["DELETE"])
@login_required
def delete_event(event_id):
    """Deleta um evento."""
    event = Event.query.get_or_404(event_id)

    # Verifica se o usuário logado é o organizador
    if event.organizer_id != g.user.id:
        return (
            jsonify(
                {
                    "error": "Acesso não autorizado. Você não é o organizador deste evento."
                }
            ),
            403,
        )

    try:
        db.session.delete(event)
        db.session.commit()
        return jsonify({"success": True, "message": "Evento removido com sucesso."})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro ao remover evento.", "details": str(e)}), 500


@app.route("/api/events/<int:event_id>/export_participants")
@login_required
def export_participants(event_id):
    """Gera e baixa um CSV da lista de participantes (HU04)."""
    event = Event.query.get_or_404(event_id)

    # Verifica se o usuário logado é o organizador do evento
    if event.organizer_id != g.user.id:
        abort(403)  # Erro de acesso proibido

    # Busca os participantes
    participants = event.participants

    # Prepara o CSV na memória
    si = io.StringIO()
    # Usamos 'excel' para garantir compatibilidade com UTF-8
    cw = csv.writer(si, dialect="excel")

    # Escreve o cabeçalho
    cw.writerow(["ID do Participante", "Nome Completo", "Email"])

    # Escreve os dados
    for participant in participants:
        cw.writerow([participant.id, participant.name, participant.email])

    output = si.getvalue()

    # Retorna o arquivo para download
    filename = f"inscritos_evento_{event.id}.csv"
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment;filename={filename}"},
    )


@app.route("/api/events/<int:event_id>/activities", methods=["POST"])
@login_required
def create_activity(event_id):
    """Permite que o organizador adicione uma atividade ao evento."""
    event = Event.query.get_or_404(event_id)

    # Verifica se o usuário logado é o organizador do evento
    if event.organizer_id != g.user.id:
        return (
            jsonify(
                {
                    "error": "Acesso não autorizado. Você não é o organizador deste evento."
                }
            ),
            403,
        )

    data = request.get_json()
    if not data:
        return jsonify({"error": "Dados JSON obrigatórios."}), 400

    required_fields = ["title", "description", "start_time", "end_time", "location"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Campo obrigatório: {field}"}), 400

    try:
        start_time = datetime.fromisoformat(data["start_time"])
        end_time = datetime.fromisoformat(data["end_time"])

        # Valida se a atividade está dentro do intervalo do evento
        if (
            start_time < event.start_date
            or end_time > event.end_date
            or end_time <= start_time
        ):
            return (
                jsonify({"error": "Horário fora do intervalo do evento ou inválido."}),
                400,
            )

        activity = Activity(
            title=data["title"],
            description=data["description"],
            start_time=start_time,
            end_time=end_time,
            location=data["location"],
            event_id=event.id,
        )
        db.session.add(activity)
        db.session.commit()
        return (
            jsonify(
                {
                    "success": True,
                    "message": "Atividade adicionada com sucesso!",
                    "activity": activity.to_dict(),
                }
            ),
            201,
        )
    except Exception as e:
        db.session.rollback()
        return (
            jsonify({"error": "Erro ao adicionar atividade.", "details": str(e)}),
            500,
        )


@app.route("/api/activities/<int:activity_id>", methods=["PUT"])
@login_required
def edit_activity(activity_id):
    """Permite que o organizador edite uma atividade."""
    activity = Activity.query.get_or_404(activity_id)
    event = activity.event

    # Verifica se o usuário logado é o organizador
    if event.organizer_id != g.user.id:
        return (
            jsonify(
                {
                    "error": "Acesso não autorizado. Você não é o organizador deste evento."
                }
            ),
            403,
        )

    data = request.get_json()
    if not data:
        return jsonify({"error": "Dados JSON obrigatórios."}), 400

    try:
        if "title" in data:
            activity.title = data["title"]
        if "description" in data:
            activity.description = data["description"]
        if "start_time" in data:
            start_time = datetime.fromisoformat(data["start_time"])
            if start_time < event.start_date or start_time > event.end_date:
                return jsonify({"error": "Horário fora do intervalo do evento."}), 400
            activity.start_time = start_time
        if "end_time" in data:
            end_time = datetime.fromisoformat(data["end_time"])
            if (
                end_time < event.start_date
                or end_time > event.end_date
                or (activity.start_time and end_time <= activity.start_time)
            ):
                return (
                    jsonify(
                        {"error": "Horário fora do intervalo do evento ou inválido."}
                    ),
                    400,
                )
            activity.end_time = end_time
        if "location" in data:
            activity.location = data["location"]

        db.session.commit()
        return jsonify(
            {
                "success": True,
                "message": "Atividade atualizada com sucesso!",
                "activity": activity.to_dict(),
            }
        )
    except Exception as e:
        db.session.rollback()
        return (
            jsonify({"error": "Erro ao atualizar atividade.", "details": str(e)}),
            500,
        )


@app.route("/api/activities/<int:activity_id>", methods=["DELETE"])
@login_required
def delete_activity(activity_id):
    """Permite que o organizador remova uma atividade."""
    activity = Activity.query.get_or_404(activity_id)

    # Verifica se o usuário logado é o organizador
    if activity.event.organizer_id != g.user.id:
        return (
            jsonify(
                {
                    "error": "Acesso não autorizado. Você não é o organizador deste evento."
                }
            ),
            403,
        )

    try:
        db.session.delete(activity)
        db.session.commit()
        return jsonify({"success": True, "message": "Atividade removida com sucesso."})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro ao remover atividade.", "details": str(e)}), 500


# --- Inscrições em Eventos (Apenas para Participantes) ---
@app.route("/api/events/<int:event_id>/inscribe", methods=["POST"])
@login_required
def inscribe(event_id):
    """Processa a inscrição de um usuário em um evento."""
    event = Event.query.get_or_404(event_id)
    now = datetime.now(timezone.utc)
    # Converte as datas do DB (naive) para aware (assumindo que são UTC)
    start_date_aware = event.inscription_start_date.replace(tzinfo=timezone.utc)
    end_date_aware = event.inscription_end_date.replace(tzinfo=timezone.utc)

    # Verificação de segurança no backend
    if not (event.status == 2 and start_date_aware <= now <= end_date_aware):
        return (
            jsonify(
                {
                    "error": "As inscrições para este evento não estão abertas no momento."
                }
            ),
            400,
        )

    # Regra de Negócio: O sistema não deve permitir que o mesmo usuário se inscreva mais de uma vez
    if event in g.user.inscribed_events:
        return jsonify({"error": "Você já está inscrito neste evento."}), 409

    try:
        g.user.inscribed_events.append(event)
        db.session.commit()
        # Envia e-mail de confirmação de inscrição
        send_email(
            subject=f"Inscrição Confirmada: {event.title}",
            recipients=[g.user.email],
            text_body=f"Olá {g.user.name},\n\nSua inscrição no evento '{event.title}' foi realizada com sucesso.",
            html_body=f"<p>Olá {g.user.name},</p><p>Sua inscrição no evento <strong>{event.title}</strong> foi realizada com sucesso.</p>",
        )
        return jsonify({"success": True, "message": "Inscrição realizada com sucesso!"})
    except Exception as e:
        db.session.rollback()
        return (
            jsonify({"error": "Erro ao processar inscrição.", "details": str(e)}),
            500,
        )


@app.route("/api/my-inscriptions")
@login_required
def my_inscriptions():
    """Retorna a lista de eventos nos quais o usuário está inscrito."""
    events = g.user.inscribed_events
    return jsonify({"events": [event.to_dict() for event in events]})


@app.route("/api/events/<int:event_id>/inscribe", methods=["DELETE"])
@login_required
def unsubscribe(event_id):
    """Processa o cancelamento da inscrição de um usuário em um evento."""
    event = Event.query.get_or_404(event_id)

    if event not in g.user.inscribed_events:
        return jsonify({"error": "Você não está inscrito neste evento."}), 400

    try:
        g.user.inscribed_events.remove(event)
        db.session.commit()
        return jsonify({"success": True, "message": "Inscrição cancelada com sucesso!"})
    except Exception as e:
        db.session.rollback()
        return (
            jsonify({"error": "Erro ao cancelar inscrição.", "details": str(e)}),
            500,
        )


# --- Submissão de Trabalhos (Apenas para Palestrantes/Autores) ---
@app.route("/api/my-submissions")
@login_required
def my_submissions():
    """Retorna a lista de trabalhos submetidos pelo usuário."""
    # O relacionamento 'submissions' em User nos dá a lista
    submissions = g.user.submissions.order_by(Submission.id.desc()).all()
    return jsonify(
        {"submissions": [submission.to_dict() for submission in submissions]}
    )


@app.route("/event/<int:event_id>/submit", methods=["GET", "POST"])
@login_required
def new_submission(event_id):
    """Página para um autor submeter um trabalho a um evento."""
    event = Event.query.get_or_404(event_id)

    # Proteção de Rota: Apenas Palestrantes/Autores (role=2) podem submeter
    if g.user.role != 2:
        flash("Apenas Palestrantes/Autores podem submeter trabalhos.", "danger")
        return redirect(url_for("view_event", event_id=event_id))

    now = datetime.now(timezone.utc)
    is_submission_open = False
    if event.submission_start_date and event.submission_end_date:
        sub_start_date = event.submission_start_date.replace(tzinfo=timezone.utc)
        sub_end_date = event.submission_end_date.replace(tzinfo=timezone.utc)
        is_submission_open = event.status == 2 and sub_start_date <= now <= sub_end_date

    if not is_submission_open:
        flash(
            "O período de submissão de trabalhos para este evento não está aberto.",
            "warning",
        )
        return redirect(url_for("view_event", event_id=event.id))

    form = SubmissionForm()
    if form.validate_on_submit():
        file = form.submission_file.data

        # Verificacão de extensão e segurança
        # Valida MIME type
        mime = magic.Magic(mime=True)
        file_mime = mime.from_buffer(file.read())
        file.seek(0)
        allowed_mimes = [
            "application/pdf",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/rtf",
            "text/rtf",
            "application/vnd.oasis.opendocument.text",
            "text/plain",
        ]
        if file_mime not in allowed_mimes:
            flash(
                "Tipo de arquivo não permitido. Apenas documentos PDF, DOC, DOCX, ODT e RTF são aceitos.",
                "danger",
            )
            return redirect(url_for("new_submission", event_id=event.id))

        # Escaneamento de vírus usando ClamAV
        try:
            cd = pyclamd.ClamdAgnostic()
            scan_result = cd.scan_stream(file.read())
            file.seek(0)
            if scan_result:
                app.logger.error(
                    f"Virus detected in uploaded file: {file.filename}, scan result: {scan_result}"
                )
                flash("Arquivo suspeito detectado. Upload rejeitado.", "danger")
                return redirect(url_for("new_submission", event_id=event.id))
        except Exception as e:
            app.logger.warning(f"ClamAV scan failed: {e}")

        filename = secure_filename(file.filename)
        upload_folder = app.config["UPLOADED_FILES_DEST"]
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)

        submission = Submission(
            title=form.title.data,
            file_path=filename,
            author_id=g.user.id,  # Associa a submissão ao usuário logado
            event_id=event.id,  # Associa ao evento atual
        )
        db.session.add(submission)
        db.session.commit()
        flash("Trabalho submetido com sucesso!", "success")
        return redirect(url_for("my_submissions"))

    return jsonify({"page": "unknown"})


@app.route("/submission/download/<int:submission_id>")
@login_required
def download_submission(submission_id):
    """Permite o download do arquivo de submissão (Autor ou Organizador)."""
    sub = Submission.query.get_or_404(submission_id)

    # Segurança: Apenas o autor ou o organizador do evento podem baixar
    if sub.author_id != g.user.id and sub.event.organizer_id != g.user.id:
        abort(403)

    try:
        # Retorna o arquivo da pasta de uploads
        return send_from_directory(
            app.config["UPLOADED_FILES_DEST"],
            sub.file_path,
            as_attachment=True,
        )
    except FileNotFoundError:
        abort(404)


@app.route("/submission/evaluate/<int:submission_id>", methods=["POST"])
@login_required
def evaluate_submission(submission_id):
    """Processa a avaliação (aprovação/rejeição) de uma submissão."""
    form = SubmissionEvalForm()
    sub = Submission.query.get_or_404(submission_id)

    # Verifica se o usuário logado é o organizador do evento da submissão
    if sub.event.organizer_id != g.user.id:
        abort(403)  # Erro de acesso proibido

    if form.validate_on_submit():
        new_status = int(form.new_status.data)
        # Status: 3=Aprovado, 4=Rejeitado
        if new_status in [3, 4]:
            sub.status = new_status
            db.session.commit()

            # Envia e-mail ao autor notificando sobre a decisão
            status_str = "Aprovado" if sub.status == 3 else "Rejeitado"
            send_email(
                subject=f"Atualização da sua Submissão: {sub.title}",
                recipients=[sub.author.email],
                text_body=f"Olá {sub.author.name},\n\nO status do seu trabalho '{sub.title}' (submetido para o evento '{sub.event.title}') foi atualizado para: {status_str}.",
                html_body=f"<p>Olá {sub.author.name},</p><p>O status do seu trabalho '<strong>{sub.title}</strong>' (submetido para o evento '<strong>{sub.event.title}</strong>') foi atualizado para: <strong>{status_str}</strong>.</p>",
            )

            flash("O status da submissão foi atualizado.", "success")
        else:
            flash("Ação inválida.", "danger")

    return redirect(url_for("view_event", event_id=sub.event_id))


@app.route("/api/submissions/<int:submission_id>/evaluate", methods=["POST"])
@login_required
def api_evaluate_submission(submission_id):
    """API para avaliar uma submissão."""
    data = request.get_json()
    if not data or "new_status" not in data:
        return jsonify({"error": "new_status required"}), 400

    sub = Submission.query.get_or_404(submission_id)

    # Verifica se o usuário logado é o organizador do evento da submissão
    if sub.event.organizer_id != g.user.id:
        return jsonify({"error": "Acesso não autorizado"}), 403

    new_status = int(data["new_status"])
    if new_status in [3, 4]:
        sub.status = new_status
        db.session.commit()

        # Envia e-mail ao autor notificando sobre a decisão
        status_str = "Aprovado" if sub.status == 3 else "Rejeitado"
        send_email(
            subject=f"Atualização da sua Submissão: {sub.title}",
            recipients=[sub.author.email],
            text_body=f"Olá {sub.author.name},\n\nO status do seu trabalho '{sub.title}' (submetido para o evento '{sub.event.title}') foi atualizado para: {status_str}.",
            html_body=f"<p>Olá {sub.author.name},</p><p>O status do seu trabalho '<strong>{sub.title}</strong>' (submetido para o evento '<strong>{sub.event.title}</strong>') foi atualizado para: <strong>{status_str}</strong>.</p>",
        )

        return jsonify({"success": True, "message": "Status atualizado"})
    else:
        return jsonify({"error": "Status inválido"}), 400


@app.route("/api/submissions/<int:submission_id>/download")
@login_required
def api_download_submission(submission_id):
    """API para download do arquivo de submissão."""
    sub = Submission.query.get_or_404(submission_id)

    # Segurança: Apenas o autor ou o organizador do evento podem baixar
    if sub.author_id != g.user.id and sub.event.organizer_id != g.user.id:
        return jsonify({"error": "Acesso não autorizado"}), 403

    try:
        # Retorna o arquivo da pasta de uploads
        return send_from_directory(
            app.config["UPLOADED_FILES_DEST"],
            sub.file_path,
            as_attachment=True,
        )
    except FileNotFoundError:
        return jsonify({"error": "Arquivo não encontrado"}), 404


# --- ROTAS LGPD ---
@app.route("/api/termos-de-uso")
def termos_de_uso():
    """Página estática para os Termos de Uso."""
    return jsonify({"content": "Termos de Uso - A implementar"})


@app.route("/api/politica-de-privacidade")
def politica_de_privacidade():
    """Página estática para a Política de Privacidade."""
    return jsonify({"content": "Política de Privacidade - A implementar"})


@app.route("/api/events/<int:event_id>/submit", methods=["POST"])
@login_required
def submit_work(event_id):
    """API para submeter um trabalho a um evento."""
    event = Event.query.get_or_404(event_id)

    # Proteção de Rota: Apenas Palestrantes/Autores (role=2) podem submeter
    if g.user.role != 2:
        return (
            jsonify({"error": "Apenas Palestrantes/Autores podem submeter trabalhos."}),
            403,
        )

    now = datetime.now(timezone.utc)
    is_submission_open = False
    if event.submission_start_date and event.submission_end_date:
        sub_start_date = event.submission_start_date.replace(tzinfo=timezone.utc)
        sub_end_date = event.submission_end_date.replace(tzinfo=timezone.utc)
        is_submission_open = event.status == 2 and sub_start_date <= now <= sub_end_date

    if not is_submission_open:
        return (
            jsonify(
                {
                    "error": "O período de submissão de trabalhos para este evento não está aberto."
                }
            ),
            400,
        )

    if "file" not in request.files:
        return jsonify({"error": "Arquivo é obrigatório."}), 400

    file = request.files["file"]
    title = request.form.get("title")

    if not title:
        return jsonify({"error": "Título é obrigatório."}), 400

    if file.filename == "":
        return jsonify({"error": "Arquivo não selecionado."}), 400

    # Validação de extensão
    if not allowed_file(file.filename):
        return (
            jsonify(
                {
                    "error": "Tipo de arquivo não suportado. Apenas PDF, DOC, DOCX, ODT e RTF são permitidos."
                }
            ),
            400,
        )

    # Valida MIME type
    mime = magic.Magic(mime=True)
    file_mime = mime.from_buffer(file.read())
    file.seek(0)
    allowed_mimes = [
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/rtf",
        "text/rtf",
        "application/vnd.oasis.opendocument.text",
        "text/plain",
    ]
    if file_mime not in allowed_mimes:
        return jsonify({"error": "Tipo de arquivo não permitido."}), 400

    # Escaneamento de vírus
    try:
        cd = pyclamd.ClamdAgnostic()
        scan_result = cd.scan_stream(file.read())
        file.seek(0)
        if scan_result:
            return jsonify({"error": "Arquivo suspeito detectado."}), 400
    except Exception as e:
        app.logger.warning(f"ClamAV scan failed: {e}")

    filename = secure_filename(file.filename)
    upload_folder = app.config["UPLOADED_FILES_DEST"]
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)

    submission = Submission(
        title=title,
        file_path=filename,
        author_id=g.user.id,
        event_id=event.id,
    )
    db.session.add(submission)
    db.session.commit()
    return (
        jsonify(
            {
                "success": True,
                "message": "Trabalho submetido com sucesso!",
                "submission": submission.to_dict(),
            }
        ),
        201,
    )
