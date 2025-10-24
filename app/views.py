from logging import warning
from flask import url_for, redirect, render_template, flash, g, abort, Response
from flask_mail import Message
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm, mail
from app.forms import (
    ActivityForm,
    RegistrationForm,
    LoginForm,
    EventForm,
    DeleteEventForm,
    InscriptionForm,
    SubmissionEvalForm,
    SubmissionForm,
    CancelInscriptionForm,
)
from app.models import Activity, Submission, User, Event
from datetime import datetime, timezone
import time, io, csv
from threading import Thread


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
@app.route("/")
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

        return render_template(
            "dashboard.html",
            title="Meu Dashboard",
            inscribed_events=inscribed_events,
            submissions=submissions,
            organized_events=organized_events,
        )

    # Se não estiver logado, mostra a página de índice padrão
    return render_template("index.html")


@app.route("/events")
def list_events():
    """Página para listar todos os eventos PÚBLICOS."""
    # Filtra os eventos para mostrar apenas os com status=2 (Publicado)
    events = Event.query.filter_by(status=2).order_by(Event.start_date.desc()).all()
    return render_template("list_events.html", events=events)


# --- Autenticação ---
@app.route("/register", methods=["GET", "POST"])
def register():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for("index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        # --- Verifica se o e-mail já existe ---
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash(
                "Este email já está registrado. Faça login ou use outro endereço.",
                "danger",
            )
            return redirect(url_for("register"))
        # --- Cria novo usuário ---
        user = User(
            name=form.name.data, email=form.email.data, role=int(form.role.data)
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        # --- Enviar E-mail de Confirmação de Registro ---
        send_email(
            subject="Bem-vindo(a) ao Eventum!",
            recipients=[user.email],
            text_body=f"Olá {user.name},\n\nSeu registro na plataforma Eventum foi realizado com sucesso.",
            html_body=f"<p>Olá {user.name},</p><p>Seu registro na plataforma Eventum foi realizado com sucesso.</p>",
        )

        flash("Registro realizado com sucesso! Faça login para continuar.", "success")
        return redirect(url_for("login"))

    return render_template("register.html", title="Registrar", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # Verifica se o utilizador existe e se a senha está correta
        if user is None or not user.check_password(form.password.data):
            flash("Email ou senha inválidos.", "danger")
            return redirect(url_for("login"))

        login_user(user)
        flash("Login realizado com sucesso!", "success")
        return redirect(url_for("index"))

    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


# --- Gestão de Eventos (Apenas para Organizadores) ---
@app.route("/event/new", methods=["GET", "POST"])
@login_required
def new_event():
    # Proteção de Rota: Apenas utilizadores com role=1 (Organizador) podem usar esta rota
    if g.user.role != 1:
        flash("Acesso não autorizado.", "danger")
        return redirect(url_for("index"))

    form = EventForm()
    if form.validate_on_submit():
        event = Event(
            title=form.title.data,
            description=form.description.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            inscription_start_date=form.inscription_start_date.data,
            inscription_end_date=form.inscription_end_date.data,
            status=int(form.status.data),
            organizer_id=g.user.id,  # Associa o evento ao utilizador logado
        )
        db.session.add(event)
        db.session.commit()
        flash("Evento criado com sucesso!", "success")
        return redirect(url_for("list_events"))

    return render_template("event_form.html", title="Novo Evento", form=form)


@app.route("/event/<int:event_id>")
def view_event(event_id):
    """Exibe os detalhes de um evento específico."""
    event = Event.query.get_or_404(event_id)
    form = InscriptionForm()
    eval_form = SubmissionEvalForm()
    delete_form = DeleteEventForm()
    activities = event.activities.order_by(Activity.start_time).all()
    # Lógica para verificar se as inscrições estão abertas
    now = datetime.now(timezone.utc)
    # Converte as datas do DB (naive) para aware (assumindo que são UTC)
    start_date = event.inscription_start_date.replace(tzinfo=timezone.utc)
    end_date = event.inscription_end_date.replace(tzinfo=timezone.utc)
    is_inscription_open = event.status == 2 and start_date <= now <= end_date
    return render_template(
        "view_event.html",
        event=event,
        form=form,
        eval_form=eval_form,
        delete_form=delete_form,
        activities=activities,
        is_inscription_open=is_inscription_open,
    )


@app.route("/event/edit/<int:event_id>", methods=["GET", "POST"])
@login_required
def edit_event(event_id):
    """Permite que o organizador edite um evento."""
    event = Event.query.get_or_404(event_id)

    # Verifica se o usuário logado é o organizador do evento
    if event.organizer_id != g.user.id:
        abort(403)  # Erro de acesso proibido

    form = EventForm(obj=event)  # Pré-popula o formulário com dados do evento
    if form.validate_on_submit():
        event.title = form.title.data
        event.description = form.description.data
        event.start_date = form.start_date.data
        event.end_date = form.end_date.data
        event.inscription_start_date = form.inscription_start_date.data
        event.inscription_end_date = form.inscription_end_date.data
        event.status = int(form.status.data)
        db.session.commit()
        flash("Evento atualizado com sucesso!", "success")
        return redirect(url_for("view_event", event_id=event.id))

    return render_template("event_form.html", title="Editar Evento", form=form)


@app.route("/event/delete/<int:event_id>", methods=["POST"])
@login_required
def delete_event(event_id):
    """Deleta um evento."""
    event = Event.query.get_or_404(event_id)
    form = DeleteEventForm()

    # Verifica se o usuário logado é o organizador
    if event.organizer_id != g.user.id:
        abort(403)

    db.session.delete(event)
    db.session.commit()
    flash("Evento removido com sucesso.", "success")
    return redirect(url_for("list_events"))


@app.route("/event/<int:event_id>/export_participants")
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


@app.route("/event/<int:event_id>/schedule", methods=["GET", "POST"])
@login_required
def manage_schedule(event_id):
    """Página para o organizador gerenciar a programação de um evento."""
    event = Event.query.get_or_404(event_id)

    # Verifica se o usuário logado é o organizador do evento
    if event.organizer_id != g.user.id:
        abort(403)  # Erro de acesso proibido

    # Injeta o objeto 'event' no construtor do formulário
    form = ActivityForm(event=event)
    activities = event.activities.order_by(Activity.start_time).all()

    if form.validate_on_submit():
        # Combina a data do evento com o horário submetido
        # Se o evento for de vários dias, é necessário permitir que o usuário escolha o dia também
        event_day = event.start_date.date()  # Aqui assumimos o primeiro dia do evento
        if event.start_date.date() != event.end_date.date():
            flash(
                "Atividades para eventos de vários dias ainda não são suportadas.",
                "warning",
            )
            return redirect(url_for("manage_schedule", event_id=event.id))
        start_time = datetime.combine(event_day, form.start_time.data)
        end_time = datetime.combine(event_day, form.end_time.data)

        # Valida se a atividade está dentro do intervalo do evento
        if (
            start_time < event.start_date
            or end_time > event.end_date
            or end_time <= start_time
        ):
            flash("Horário fora do intervalo do evento ou inválido.", "danger")
        else:
            activity = Activity(
                title=form.title.data,
                description=form.description.data,
                start_time=start_time,
                end_time=end_time,
                location=form.location.data,
                event_id=event.id,
            )
            db.session.add(activity)
            db.session.commit()
            flash("Atividade adicionada com sucesso!", "success")
            return redirect(url_for("manage_schedule", event_id=event.id))

    # Busca as atividades já existentes para listá-las na página
    activities = event.activities.order_by(Activity.start_time).all()

    return render_template(
        "manage_schedule.html",
        title="Gerenciar Programação",
        form=form,
        event=event,
        activities=activities,
    )


# --- Inscrições em Eventos (Apenas para Participantes) ---
@app.route("/event/inscribe/<int:event_id>", methods=["POST"])
@login_required
def inscribe(event_id):
    """Processa a inscrição de um usuário em um evento."""
    form = InscriptionForm()
    event = Event.query.get_or_404(event_id)
    now = datetime.now(timezone.utc)
    # Converte as datas do DB (naive) para aware (assumindo que são UTC)
    start_date_aware = event.inscription_start_date.replace(tzinfo=timezone.utc)
    end_date_aware = event.inscription_end_date.replace(tzinfo=timezone.utc)

    # Verificação de segurança no backend
    if not (event.status == 2 and start_date_aware <= now <= end_date_aware):
        flash("As inscrições para este evento não estão abertas no momento.", "warning")
        return redirect(url_for("view_event", event_id=event_id))

    if form.validate_on_submit():
        # Regra de Negócio: O sistema não deve permitir que o mesmo usuário se inscreva mais de uma vez
        if event in g.user.inscribed_events:
            flash("Você já está inscrito neste evento.", "warning")
        else:
            g.user.inscribed_events.append(event)
            db.session.commit()
            # Envia e-mail de confirmação de inscrição
            send_email(
                subject=f"Inscrição Confirmada: {event.title}",
                recipients=[g.user.email],
                text_body=f"Olá {g.user.name},\n\nSua inscrição no evento '{event.title}' foi realizada com sucesso.",
                html_body=f"<p>Olá {g.user.name},</p><p>Sua inscrição no evento <strong>{event.title}</strong> foi realizada com sucesso.</p>",
            )
            flash("Inscrição realizada com sucesso!", "success")
    else:
        flash("Ocorreu um erro ao processar sua inscrição.", "danger")

    return redirect(url_for("view_event", event_id=event_id))


@app.route("/my-inscriptions")
@login_required
def my_inscriptions():
    """Exibe a lista de eventos nos quais o usuário está inscrito."""
    # O relacionamento 'inscribed_events' já nos dá a lista de eventos do usuário logado
    events = g.user.inscribed_events
    form = CancelInscriptionForm()
    return render_template(
        "my_inscriptions.html",
        title="Minhas Inscrições",
        events=events,
        form=form,
    )


@app.route("/event/unsubscribe/<int:event_id>", methods=["POST"])
@login_required
def unsubscribe(event_id):
    """Processa o cancelamento da inscrição de um usuário em um evento."""
    form = CancelInscriptionForm()
    event = Event.query.get_or_404(event_id)

    if form.validate_on_submit():
        # Verifica se o usuário está realmente inscrito
        if event not in g.user.inscribed_events:
            flash("Você não está inscrito neste evento.", "danger")
            return redirect(url_for("my_inscriptions"))

        # Remove a associação
        g.user.inscribed_events.remove(event)
        db.session.commit()
        flash("Inscrição cancelada com sucesso.", "success")
    else:
        # Se o form não validar (ex: CSRF inválido), redireciona por segurança
        flash("Ocorreu um erro ao processar sua solicitação.", "danger")

    return redirect(url_for("my_inscriptions"))


# --- Submissão de Trabalhos (Apenas para Palestrantes/Autores) ---
@app.route("/my-submissions")
@login_required
def my_submissions():
    """Exibe a lista de trabalhos submetidos pelo usuário."""
    # O relacionamento 'submissions' em User nos dá a lista
    submissions = g.user.submissions.order_by(Submission.id.desc()).all()
    return render_template(
        "my_submissions.html", title="Minhas Submissões", submissions=submissions
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

    form = SubmissionForm()
    if form.validate_on_submit():
        submission = Submission(
            title=form.title.data,
            abstract=form.abstract.data,
            author_id=g.user.id,  # Associa a submissão ao usuário logado
            event_id=event.id,  # Associa ao evento atual
        )
        db.session.add(submission)
        db.session.commit()
        flash("Trabalho submetido com sucesso!", "success")
        return redirect(url_for("my_submissions"))

    return render_template(
        "submission_form.html", title="Submeter Trabalho", form=form, event=event
    )


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


# --- ROTAS LGPD ---
@app.route("/termos-de-uso")
def termos_de_uso():
    """Página estática para os Termos de Uso."""
    return render_template("termos_de_uso.html", title="Termos de Uso")


@app.route("/politica-de-privacidade")
def politica_de_privacidade():
    """Página estática para a Política de Privacidade."""
    return render_template(
        "politica_de_privacidade.html", title="Política de Privacidade"
    )
