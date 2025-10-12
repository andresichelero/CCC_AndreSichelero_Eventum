class Config(object):
    """
    Configuration base, for all environments.
    """

    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:password@localhost/postgres"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BOOTSTRAP_FONTAWESOME = True
    SECRET_KEY = "password"
    CSRF_ENABLED = True


class ProductionConfig(Config):
    # A URI do banco de dados de produção seria diferente, mas por enquanto herda da base
    pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
