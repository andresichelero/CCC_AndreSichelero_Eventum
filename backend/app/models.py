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
    # Permite que o perfil seja listado na funcionalidade "Quem Vai"
    allow_public_profile = db.Column(db.Boolean, nullable=False, default=False)

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

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "allow_public_profile": self.allow_public_profile,
        }

    def __repr__(self):
        return f"<User {self.name}>"


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    inscription_start_date = db.Column(db.DateTime, nullable=False)
    inscription_end_date = db.Column(db.DateTime, nullable=False)
    # Chave estrangeira para o organizador do evento
    organizer_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    # Status: 1=Rascunho, 2=Publicado
    status = db.Column(db.SmallInteger, nullable=False, default=1)
    # Relacionamento: Programação do evento
    activities = db.relationship("Activity", backref="event", lazy="dynamic")
    # Relacionamento: Submissões para este evento
    submissions = db.relationship("Submission", backref="event", lazy="dynamic")
    submission_start_date = db.Column(db.DateTime, nullable=True)  # Permitindo nulo por enquanto
    submission_end_date = db.Column(db.DateTime, nullable=True)  # Permitindo nulo por enquanto
    workload = db.Column(db.Integer, nullable=True, default=0)  # Carga horária (em horas)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "inscription_start_date": self.inscription_start_date.isoformat() if self.inscription_start_date else None,
            "inscription_end_date": self.inscription_end_date.isoformat() if self.inscription_end_date else None,
            "organizer": self.organizer.to_dict(),
            "organizer_id": self.organizer_id,
            "status": self.status,
            "submission_start_date": self.submission_start_date.isoformat() if self.submission_start_date else None,
            "submission_end_date": self.submission_end_date.isoformat() if self.submission_end_date else None,
            "workload": self.workload
        }

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

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "location": self.location,
            "event_id": self.event_id
        }

    def __repr__(self):
        return f"<Activity {self.title}>"


class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)  # Caminho do arquivo submetido
    # Status: 1=Submetido, 2=Em avaliação, 3=Aprovado, 4=Rejeitado
    status = db.Column(db.SmallInteger, nullable=False, default=1)
    # Chave estrangeira para o autor
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    # Chave estrangeira para o evento
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "file_path": self.file_path,
            "status": self.status,
            "author": self.author.to_dict(),
            "author_id": self.author_id,
            "event": self.event.to_dict(),
            "event_id": self.event_id
        }

    def __repr__(self):
        return f"<Submission {self.title}>"
