from flask import Blueprint, request, jsonify
from app.models import Imovel
from app.db import db

bp = Blueprint("imoveis", __name__)

@bp.get("/")
def listar_imoveis():
    imoveis = Imovel.query.all()
    return jsonify([{"id": i.id, "tipo": i.tipo, "cidade": i.cidade} for i in imoveis])
