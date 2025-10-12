from app import db
from werkzeug.security import generate_password_hash, check_password_hash

# Tabela associativa para a relação muitos-para-muitos entre Usuários (participantes) e Eventos
inscriptions = db.Table(
    "inscriptions",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("event_id", db.Integer, db.ForeignKey("event.id"), primary_key=True),
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    # Papel do usuário: 1=Organizador, 2=Palestrante/Autor, 3=Participante
    role = db.Column(db.SmallInteger, nullable=False, default=3)

    # Relacionamento: Eventos que este usuário organizou
    organized_events = db.relationship("Event", backref="organizer", lazy="dynamic")
    # Relacionamento: Submissões feitas por este usuário
    submissions = db.relationship("Submission", backref="author", lazy="dynamic")
    # Relacionamento: Eventos nos quais este usuário está inscrito
    inscribed_events = db.relationship(
        "Event",
        secondary=inscriptions,
        lazy="subquery",
        backref=db.backref("participants", lazy=True),
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Métodos exigidos pelo Flask-Login
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return f"<User {self.name}>"


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    # Chave estrangeira para o organizador do evento
    organizer_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    # Relacionamento: Programação do evento
    activities = db.relationship("Activity", backref="event", lazy="dynamic")
    # Relacionamento: Submissões para este evento
    submissions = db.relationship("Submission", backref="event", lazy="dynamic")

    def __repr__(self):
        return f"<Event {self.title}>"


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    description = db.Column(db.Text)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(250))  # Ex: "Auditório A"
    # Chave estrangeira para o evento ao qual a atividade pertence
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"), nullable=False)

    def __repr__(self):
        return f"<Activity {self.title}>"


class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    abstract = db.Column(db.Text, nullable=False)  # Resumo do trabalho
    # Status: 1=Submetido, 2=Em avaliação, 3=Aprovado, 4=Rejeitado
    status = db.Column(db.SmallInteger, nullable=False, default=1)
    # Chave estrangeira para o autor
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    # Chave estrangeira para o evento
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"), nullable=False)

    def __repr__(self):
        return f"<Submission {self.title}>"
