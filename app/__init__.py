import os
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

db_url = os.environ.get("SQLALCHEMY_DATABASE_URI")
if not db_url:
    db_url = "sqlite:///default.db"

app.config["SQLALCHEMY_DATABASE_URI"] = db_url
# Inicialização das Extensões
db = SQLAlchemy(app)
migrate = Migrate(app, db)
lm = LoginManager(app)
bootstrap = Bootstrap(app)

# Importa as views e modelos no final para evitar importações circulares
from app import views, models
