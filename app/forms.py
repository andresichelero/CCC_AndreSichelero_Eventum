from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    DateTimeField,
    PasswordField,
    SubmitField,
    SelectField,
    HiddenField
)
from wtforms.validators import DataRequired, Email, EqualTo, Length


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Senha", validators=[DataRequired()])
    submit = SubmitField("Entrar")


class RegistrationForm(FlaskForm):
    name = StringField(
        "Nome Completo", validators=[DataRequired(), Length(min=3, max=150)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    # Papel do usuário: 1=Organizador, 2=Palestrante/Autor, 3=Participante
    role = SelectField(
        "Eu sou",
        choices=[
            ("3", "Participante"),
            ("2", "Palestrante/Autor"),
            ("1", "Organizador"),
        ],
        validators=[DataRequired()],
    )
    password = PasswordField("Senha", validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField(
        "Repetir Senha",
        validators=[
            DataRequired(),
            EqualTo("password", message="As senhas devem ser iguais."),
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
    submit = SubmitField("Salvar Evento")


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
    abstract = TextAreaField("Resumo (Abstract)", validators=[DataRequired()])
    submit = SubmitField("Enviar Submissão")


class SubmissionEvalForm(FlaskForm):
    # Usaremos um campo oculto para passar o novo status
    new_status = HiddenField("Novo Status")
    submit = SubmitField("Confirmar")  # O texto deste botão será alterado no template
