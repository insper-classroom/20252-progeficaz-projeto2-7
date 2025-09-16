from flask import Flask, request
import views

app = Flask(__name__)

@app.route('/imoveis', methods=['GET'])
def listar_imoveis():
    resultado = views.get_imoveis()
    return resultado[0], resultado[1]

@app.route('/imoveis/<int:id>', methods=['GET'])
def obter_imovel(id):
    resultado = views.get_id(id)
    return resultado[0], resultado[1]

@app.route('/imoveis', methods=['POST'])
def cadastrar_imovel():
    imovel = request.get_json()
    resultado = views.novo_imovel(imovel)
    return resultado[0], resultado[1]

@app.route('/imoveis/<int:id>', methods=['PUT'])
def atualizar_imovel(id):
    imovel = request.get_json()
    resultado = views.att_imovel(id, imovel)
    return resultado[0], resultado[1]

@app.route('/imoveis/<int:id>', methods=['DELETE'])
def excluir_imovel(id):
    resultado = views.remove_imovel(id)
    return resultado[0], resultado[1]

@app.route('/imoveis/tipo/<string:tipo>', methods=['GET'])
def buscar_por_tipo(tipo):
    resultado = views.list_tipo(tipo)
    return resultado[0], resultado[1]

@app.route('/imoveis/cidade/<string:cidade>', methods=['GET'])
def buscar_por_cidade(cidade):
    resultado = views.list_cidade(cidade)
    return resultado[0], resultado[1]


if __name__ == '__main__':
    app.run(debug=True)
