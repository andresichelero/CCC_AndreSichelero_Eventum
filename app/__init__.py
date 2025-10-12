from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

# Inicialização do App
app = Flask(__name__)
app.config.from_object(
    "app.configuration.DevelopmentConfig"
)  # Carrega a config de desenvolvimento

# Inicialização das Extensões
db = SQLAlchemy(app)
migrate = Migrate(app, db)
lm = LoginManager(app)
bootstrap = Bootstrap(app)

# Importa as views e modelos no final para evitar importações circulares
from app import views, models
