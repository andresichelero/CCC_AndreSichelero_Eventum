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
    # Papel do usuário: 1=Organizador, 2=Palestrante/Autor, 3=Participante, 4=Professor
    role = db.Column(db.SmallInteger, nullable=False, default=3)
    # Permite que o perfil seja listado na funcionalidade "Quem Vai"
    allow_public_profile = db.Column(db.Boolean, nullable=False, default=False)
    # Token para reset de senha
    reset_token = db.Column(db.String(256), nullable=True)

    # Vínculos Acadêmicos
    curso_id = db.Column(db.Integer, db.ForeignKey("curso.id"), nullable=True)
    turma_id = db.Column(db.Integer, db.ForeignKey("turma.id"), nullable=True)

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
            "faculdade_id": self.curso.faculdade_id if self.curso else None,
            "faculdade": (
                self.curso.faculdade.to_dict()
                if self.curso and self.curso.faculdade
                else None
            ),
            "curso_id": self.curso_id,
            "curso": self.curso.to_dict() if self.curso else None,
            "turma_id": self.turma_id,
            "turma": self.turma.to_dict() if self.turma else None,
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
    submission_start_date = db.Column(
        db.DateTime, nullable=True
    )  # Permitindo nulo por enquanto
    submission_end_date = db.Column(
        db.DateTime, nullable=True
    )  # Permitindo nulo por enquanto
    workload = db.Column(
        db.Integer, nullable=True, default=0
    )  # Carga horária (em horas)
    # Vínculos Acadêmicos
    # Evento pode ser organizado por um Curso (ex: Semana da Computação)
    curso_id = db.Column(db.Integer, db.ForeignKey("curso.id"), nullable=True)
    # Ou por uma Faculdade (ex: Semana da Engenharia)
    faculdade_id = db.Column(db.Integer, db.ForeignKey("faculdade.id"), nullable=True)
    # Ou por uma Turma (ex: Evento de uma turma específica)
    turma_id = db.Column(db.Integer, db.ForeignKey("turma.id"), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "inscription_start_date": (
                self.inscription_start_date.isoformat()
                if self.inscription_start_date
                else None
            ),
            "inscription_end_date": (
                self.inscription_end_date.isoformat()
                if self.inscription_end_date
                else None
            ),
            "organizer": self.organizer.to_dict(),
            "organizer_id": self.organizer_id,
            "status": self.status,
            "submission_start_date": (
                self.submission_start_date.isoformat()
                if self.submission_start_date
                else None
            ),
            "submission_end_date": (
                self.submission_end_date.isoformat()
                if self.submission_end_date
                else None
            ),
            "workload": self.workload,
            "curso_id": self.curso_id,
            "curso": self.curso.to_dict() if self.curso else None,
            "faculdade_id": self.faculdade_id,
            "faculdade": self.faculdade.to_dict() if self.faculdade else None,
            "turma_id": self.turma_id,
            "turma": self.turma.to_dict() if self.turma else None,
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
            "event_id": self.event_id,
        }

    def __repr__(self):
        return f"<Activity {self.title}>"


class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    file_path = db.Column(
        db.String(255), nullable=False
    )  # Caminho do arquivo submetido
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
            "event_id": self.event_id,
        }

    def __repr__(self):
        return f"<Submission {self.title}>"


class Faculdade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)  # Descrição da faculdade
    address = db.Column(db.String(300), nullable=True)  # Endereço da faculdade

    # Relacionamento: Cursos desta faculdade
    cursos = db.relationship("Curso", backref="faculdade", lazy="dynamic")
    # Relacionamento: Eventos organizados por esta faculdade
    events = db.relationship("Event", backref="faculdade", lazy="dynamic")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "address": self.address,
        }

    def __repr__(self):
        return f"<Faculdade {self.name}>"


class Curso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)  # Descrição do curso
    duration_years = db.Column(db.Integer, nullable=True)  # Duração em anos

    # Chave estrangeira para a Faculdade
    faculdade_id = db.Column(db.Integer, db.ForeignKey("faculdade.id"), nullable=False)

    # Relacionamento: Turmas deste curso
    turmas = db.relationship("Turma", backref="curso", lazy="dynamic")
    # Relacionamento: Usuários (alunos/professores) neste curso
    users = db.relationship("User", backref="curso", lazy="dynamic")
    # Relacionamento: Eventos organizados por este curso
    events = db.relationship("Event", backref="curso", lazy="dynamic")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "duration_years": self.duration_years,
            "faculdade_id": self.faculdade_id,
        }

    def __repr__(self):
        return f"<Curso {self.name}>"


class Turma(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Ex: "Comp2025/1 - IA"
    academic_year = db.Column(db.String(10), nullable=True)  # Ex: "2024/2025"
    semester = db.Column(db.SmallInteger, nullable=True)  # 1 ou 2
    is_public = db.Column(db.Boolean, nullable=False, default=False)  # Se aparece na lista pública

    # Chave estrangeira para o Curso
    curso_id = db.Column(db.Integer, db.ForeignKey("curso.id"), nullable=False)

    # Relacionamento: Usuários (alunos) nesta turma
    users = db.relationship("User", backref="turma", lazy="dynamic")

    # Relacionamento: Eventos organizados por esta turma
    events = db.relationship("Event", backref="turma", lazy="dynamic")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "academic_year": self.academic_year,
            "semester": self.semester,
            "is_public": self.is_public,
            "curso_id": self.curso_id,
        }

    def __repr__(self):
        return f"<Turma {self.name}>"
