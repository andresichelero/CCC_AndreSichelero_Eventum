from flask import url_for, redirect, render_template, flash, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from app.forms import RegistrationForm, LoginForm, EventForm
from app.models import User, Event


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
    # Se o utilizador já estiver logado, redireciona para a página inicial
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for("index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            name=form.name.data, email=form.email.data, role=int(form.role.data)
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Registo realizado com sucesso! Faça o login para continuar.")
        return redirect(url_for("login"))

    return render_template("register.html", title="Registar", form=form)


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

    return render_template("new_event.html", title="Novo Evento", form=form)
