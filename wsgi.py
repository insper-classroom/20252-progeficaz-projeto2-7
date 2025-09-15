from flask import Flask, jsonify


app = Flask(__name__)


def connect_db():
    #Fake DB connection (sera mockada nos testes)
    pass

