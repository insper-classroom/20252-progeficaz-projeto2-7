from .db import db

class Imovel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(200), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    area = db.Column(db.Float, nullable=False)
    quartos = db.Column(db.Integer, nullable=False)
    banheiros = db.Column(db.Integer, nullable=False)
    vagas = db.Column(db.Integer, nullable=False)
    descricao = db.Column(db.Text)
