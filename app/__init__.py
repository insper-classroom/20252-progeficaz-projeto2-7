import os
from flask import Flask
from .db import db
from .routes.imoveis import bp as imoveis_bp

def create_app(test_config=None):
    app = Flask(__name__)

    # Configuração do banco
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        test_config.get("SQLALCHEMY_DATABASE_URI")
        if test_config and "SQLALCHEMY_DATABASE_URI" in test_config
        else os.getenv("DATABASE_URL", "sqlite:///dev.db")
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    if test_config:
        app.config.update(test_config)

    # Inicializa extensões
    db.init_app(app)

    # Registra rotas
    app.register_blueprint(imoveis_bp, url_prefix="/imoveis")

    return app
