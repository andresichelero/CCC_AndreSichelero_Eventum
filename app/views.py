from flask import url_for, redirect, render_template, flash, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from app.forms import (
    RegistrationForm,
    LoginForm,
    EventForm,
    DeleteEventForm,
    InscriptionForm,
    SubmissionForm,
)
from app.models import Submission, User, Event


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
    # Futuramente, esta página irá listar os eventos públicos
    return render_template("index.html")


@app.route("/events")
def list_events():
    # Página para listar todos os eventos
    events = Event.query.order_by(Event.start_date.desc()).all()
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
            flash("Este email já está registrado. Faça login ou use outro endereço.")
            return redirect(url_for("register"))

        # --- Cria novo usuário ---
        user = User(
            name=form.name.data, email=form.email.data, role=int(form.role.data)
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Registro realizado com sucesso! Faça login para continuar.")
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
            flash("Email ou senha inválidos.")
            return redirect(url_for("login"))

        login_user(user)
        flash("Login realizado com sucesso!")
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
    # Proteção de Rota: Apenas utilizadores com role=1 (Organizador) podem aceder
    if g.user.role != 1:
        flash("Acesso não autorizado.")
        return redirect(url_for("index"))

    form = EventForm()
    if form.validate_on_submit():
        event = Event(
            title=form.title.data,
            description=form.description.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            organizer_id=g.user.id,  # Associa o evento ao utilizador logado
        )
        db.session.add(event)
        db.session.commit()
        flash("Evento criado com sucesso!")
        return redirect(url_for("list_events"))

    return render_template("event_form.html", title="Novo Evento", form=form)


@app.route("/event/<int:event_id>")
def view_event(event_id):
    """Exibe os detalhes de um evento específico."""
    event = Event.query.get_or_404(event_id)
    form = InscriptionForm()
    delete_form = DeleteEventForm()
    return render_template("view_event.html", event=event, form=form, delete_form=delete_form)


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
        db.session.commit()
        flash("Evento atualizado com sucesso!")
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
    flash("Evento removido com sucesso.")
    return redirect(url_for("list_events"))

# --- Inscrições em Eventos (Apenas para Participantes) ---

@app.route("/event/inscribe/<int:event_id>", methods=["POST"])
@login_required
def inscribe(event_id):
    """Processa a inscrição de um usuário em um evento."""
    form = InscriptionForm()
    event = Event.query.get_or_404(event_id)

    if form.validate_on_submit():
        # Regra de Negócio: O sistema não deve permitir que o mesmo usuário se inscreva mais de uma vez [cite: 57]
        if event in g.user.inscribed_events:
            flash("Você já está inscrito neste evento.")
        else:
            g.user.inscribed_events.append(event)
            db.session.commit()
            flash(
                "Inscrição realizada com sucesso!"
            )  # Critério de Aceite: exibir uma mensagem de confirmação [cite: 57]
    else:
        flash("Ocorreu um erro ao processar sua inscrição.")

    return redirect(url_for("view_event", event_id=event_id))


@app.route("/my-inscriptions")
@login_required
def my_inscriptions():
    """Exibe a lista de eventos nos quais o usuário está inscrito."""
    # O relacionamento 'inscribed_events' já nos dá a lista de eventos do usuário logado
    events = g.user.inscribed_events
    return render_template(
        "my_inscriptions.html", title="Minhas Inscrições", events=events
    )


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
        flash("Apenas Palestrantes/Autores podem submeter trabalhos.")
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
        flash("Trabalho submetido com sucesso!")
        return redirect(url_for("my_submissions"))

    return render_template(
        "submission_form.html", title="Submeter Trabalho", form=form, event=event
    )
