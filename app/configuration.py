import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env na raiz do projeto
basedir = os.path.abspath(os.path.dirname(__file__))
dotenv_path = os.path.join(os.path.dirname(basedir), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


class Config(object):
    """
    Configuration base, for all environments.
    """

    # DEBUG será sobrescrito pela config de Development/Production
    DEBUG = False
    TESTING = False

    # Carrega a SECRET_KEY da variável de ambiente.
    # O fallback é fraco e serve apenas para dev se o .env não for encontrado.
    SECRET_KEY = os.environ.get("SECRET_KEY") or "uma-senha-padrao-fraca-para-dev"

    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL")
        or "postgresql://postgres:password@localhost/postgres"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BOOTSTRAP_FONTAWESOME = True
    CSRF_ENABLED = True

    # --- CONFIGURAÇÃO DE E-MAIL ---
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "sandbox.smtp.mailtrap.io")
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", "nao-responda@upf.eventum.br")


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SECRET_KEY = os.environ.get("SECRET_KEY")


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
