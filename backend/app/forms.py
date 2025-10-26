from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    DateTimeField,
    TimeField,
    PasswordField,
    SubmitField,
    SelectField,
    HiddenField,
    BooleanField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    ValidationError,
    AnyOf,
    Optional,
)
from datetime import datetime
from flask_wtf.file import FileField, FileRequired

# Validador customizado para tipos de arquivo permitidos para submissão
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'odt', 'rtf'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_file_extension(form, field):
    if field.data:
        filename = field.data.filename
        if not allowed_file(filename):
            raise ValidationError('Tipo de arquivo não suportado. Apenas PDF, DOC, DOCX, ODT e RTF são permitidos.')


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Senha", validators=[DataRequired()])
    submit = SubmitField("Entrar")


class RegistrationForm(FlaskForm):
    name = StringField(
        "Nome Completo",
        validators=[
            DataRequired(message="Este campo é obrigatório."),
            Length(
                min=3,
                max=150,
                message="O nome deve ter entre 3 e 150 caracteres.",
            ),
        ],
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Este campo é obrigatório."),
            Email(message="Por favor, insira um email válido."),
        ],
    )
    # Papel do usuário: 1=Organizador, 2=Palestrante/Autor, 3=Participante
    role = SelectField(
        "Eu sou",
        choices=[
            ("3", "Participante"),
            ("2", "Palestrante/Autor"),
            ("1", "Organizador"),
        ],
        validators=[DataRequired(message="Por favor, selecione um perfil.")],
    )
    password = PasswordField(
        "Senha",
        validators=[
            DataRequired(message="Este campo é obrigatório."),
            Length(min=6, message="A senha deve ter pelo menos 6 caracteres."),
        ],
    )
    password2 = PasswordField(
        "Repetir Senha",
        validators=[
            DataRequired(message="Este campo é obrigatório."),
            EqualTo("password", message="As senhas devem ser iguais."),
        ],
    )
    accept_terms = BooleanField(
        "Eu li e aceito os termos e a política de privacidade.",
        validators=[
            AnyOf(
                [True],
                message="Você precisa aceitar os Termos de Uso e a Política de Privacidade para continuar.",
            ),
            DataRequired(message="Este campo é obrigatório."),
        ],
    )
    submit = SubmitField("Registrar")


class EventForm(FlaskForm):
    title = StringField(
        "Título do Evento", validators=[DataRequired(), Length(max=250)]
    )
    description = TextAreaField("Descrição")
    start_date = DateTimeField(
        "Data de Início", format="%d/%m/%Y %H:%M", validators=[DataRequired()]
    )
    end_date = DateTimeField(
        "Data de Fim", format="%d/%m/%Y %H:%M", validators=[DataRequired()]
    )
    inscription_start_date = DateTimeField(
        "Início das Inscrições", format="%d/%m/%Y %H:%M", validators=[DataRequired()]
    )
    inscription_end_date = DateTimeField(
        "Fim das Inscrições", format="%d/%m/%Y %H:%M", validators=[DataRequired()]
    )
    submission_start_date = DateTimeField(
        "Início das Submissões", format="%d/%m/%Y %H:%M", validators=[Optional()]
    )
    submission_end_date = DateTimeField(
        "Fim das Submissões", format="%d/%m/%Y %H:%M", validators=[Optional()]
    )
    status = SelectField(
        "Status",
        choices=[("1", "Rascunho"), ("2", "Publicado")],
        validators=[DataRequired()],
    )
    submit = SubmitField("Salvar Evento")

    # Validador customizado
    def validate_end_date(self, field):
        if self.start_date.data and field.data:
            if field.data <= self.start_date.data:
                raise ValidationError(
                    "A data de fim do evento deve ser posterior à data de início."
                )

    # Validador customizado
    def validate_inscription_end_date(self, field):
        if self.inscription_start_date.data and field.data:
            if field.data <= self.inscription_start_date.data:
                raise ValidationError(
                    "A data de fim das inscrições deve ser posterior à data de início das inscrições."
                )

    def validate_submission_end_date(self, field):
        """Valida se a data de fim da submissão é após a de início."""
        if self.submission_start_date.data and field.data:
            if field.data <= self.submission_start_date.data:
                raise ValidationError(
                    "A data de fim das submissões deve ser posterior à data de início."
                )


class DeleteEventForm(FlaskForm):
    """
    Formulário vazio usado apenas para a proteção CSRF do botão de remover.
    """

    submit = SubmitField("Remover")


class InscriptionForm(FlaskForm):
    submit = SubmitField("Inscrever-se neste Evento")


class SubmissionForm(FlaskForm):
    title = StringField(
        "Título do Trabalho", validators=[DataRequired(), Length(max=250)]
    )
    
    submission_file = FileField(
        "Arquivo do Trabalho (PDF, DOCX, etc.)",
        validators=[FileRequired(message="É necessário enviar um arquivo."), validate_file_extension]
    )
    
    submit = SubmitField("Enviar Submissão")


class SubmissionEvalForm(FlaskForm):
    # Usaremos um campo oculto para passar o novo status
    new_status = HiddenField("Novo Status")
    submit = SubmitField("Confirmar")  # O texto deste botão será alterado no template


class ActivityForm(FlaskForm):
    title = StringField(
        "Título da Atividade", validators=[DataRequired(), Length(max=250)]
    )
    description = TextAreaField("Descrição")
    day = SelectField("Dia da Atividade", choices=[], validators=[DataRequired()])
    start_time = TimeField(
        "Horário de Início", format="%H:%M", validators=[DataRequired()]
    )
    end_time = TimeField("Horário de Fim", format="%H:%M", validators=[DataRequired()])
    location = StringField(
        "Local (Ex: Auditório A, Sala 102)",
        validators=[DataRequired(), Length(max=250)],
    )
    submit = SubmitField("Salvar Atividade")

    def __init__(self, *args, **kwargs):
        """
        Construtor customizado para aceitar o objeto 'event'.
        """
        # Remove 'event' dos kwargs antes de passar
        self.event = kwargs.pop("event", None)
        super(ActivityForm, self).__init__(*args, **kwargs)

        # Popular opções de dia com base nas datas do evento
        if self.event:
            from datetime import timedelta
            choices = []
            current = self.event.start_date.date()
            end = self.event.end_date.date()
            while current <= end:
                choices.append((current.isoformat(), current.strftime('%d/%m/%Y')))
                current += timedelta(days=1)
            self.day.choices = choices

        # Se estiver editando, definir o dia da atividade
        if self.event and hasattr(self, 'start_time') and self.start_time.data:
            pass  # WTForms já popula obj, mas precisamos definir o dia

        # Definir dia com base no objeto, se disponível
        if self.event and self.day.choices:
            obj = kwargs.get('obj')
            if obj and hasattr(obj, 'start_time'):
                self.day.data = obj.start_time.date().isoformat()

    # Validador customizado
    def validate_start_time(self, field):
        """
        Valida se o horário de início está dentro do período do evento.
        """
        if self.event and field.data and self.day.data:
            # Combina a data selecionada com a hora do formulário
            selected_day = datetime.fromisoformat(self.day.data).date()
            activity_start_dt = datetime.combine(selected_day, field.data)

            # Compara o datetime resultante com os limites do evento
            if not (self.event.start_date <= activity_start_dt <= self.event.end_date):
                raise ValidationError(
                    "O horário de início da atividade deve estar dentro do período do evento."
                )

    # Validador customizado
    def validate_end_time(self, field):
        """
        Valida se o horário de fim é após o início e está dentro do período do evento.
        """
        if self.start_time.data and field.data and self.day.data:
            selected_day = datetime.fromisoformat(self.day.data).date()
            # 1. Valida se o fim é depois do início
            if field.data <= self.start_time.data:
                raise ValidationError(
                    "O horário de fim deve ser posterior ao horário de início."
                )

            # 2. Valida se o fim está dentro do período do evento
            if self.event:
                activity_end_dt = datetime.combine(selected_day, field.data)

                if not (
                    self.event.start_date <= activity_end_dt <= self.event.end_date
                ):
                    raise ValidationError(
                        "O horário de fim da atividade deve estar dentro do período do evento."
                    )


class DeleteActivityForm(FlaskForm):
    """
    Formulário vazio para CSRF do botão de remover atividade.
    """
    submit = SubmitField("Remover")


class CancelInscriptionForm(FlaskForm):
    """
    Formulário vazio usado apenas para a proteção CSRF do botão de
    cancelamento de inscrição.
    """

    submit = SubmitField("Cancelar Inscrição")  # O botão real estará no template
