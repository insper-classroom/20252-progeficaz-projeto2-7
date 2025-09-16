from flask import Flask, jsonify, request
import os
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

config = {
    'host': os.getenv('DB_HOST', 'localhost'),  # Obtém o host do banco de dados da variável de ambiente
    'user': os.getenv('DB_USER'),  # Obtém o usuário do banco de dados da variável de ambiente
    'password': os.getenv('DB_PASSWORD'),  # Obtém a senha do banco de dados da variável de ambiente
    'database': os.getenv('DB_NAME', 'db_escola'),  # Obtém o nome do banco de dados da variável de ambiente
    'port': int(os.getenv('DB_PORT', 3306)),  # Obtém a porta do banco de dados da variável de ambiente
    'ssl_ca': os.getenv('SSL_CA_PATH')  # Caminho para o certificado SSL
}


def connect_db():
    """Estabelece a conexão com o banco de dados usando as configurações fornecidas."""
    try:
        # Tenta estabelecer a conexão com o banco de dados usando mysql-connector-python
        conn = mysql.connector.connect(**config)
        if conn.is_connected():
            return conn
    except Error as err:
        # Em caso de erro, imprime a mensagem de erro
        print(f"Erro: {err}")
        return None
    
@app.route("/")
def home():
    return "Servidor Flask rodando 🚀"

@app.route("/imoveis", methods=["GET"])
def get_imoveis():
    conn = connect_db()
    
    if conn is None:
        resp = {"erro": "Ocorreu um erro ao conectar com o banco de dados"}
        return resp, 500
    
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM imoveis')
    results = cursor.fetchall()
    
    if not results:
        resp = {"erro": "Nenhum imóvel encontrado"}
        return resp, 404 
    else:
        imoveis = []
        for imovel in results:
            imovel_dict = {
                "id": imovel[0],
                "logradouro": imovel[1],
                "tipo_logradouro": imovel[2],
                "bairro": imovel[3],
                "cidade": imovel[4],
                "cep": imovel[5],
                "tipo": imovel[6],
                "valor": imovel[7],
                "data_aquisicao": imovel[8]
            }
            imoveis.append(imovel_dict)
        resp = {"imoveis": imoveis}
        return resp, 200
    
@app.route("/imoveis/<int:imovel_id>", methods = ['GET'])
def get_imovel_id(imovel_id):
    conn = connect_db()
    if conn is None:
        resp = {"erro": "Ocorreu um erro ao conectar com o servidor"}
        return resp, 500
    
    cursor = conn.cursor()
    sql = 'SELECT * FROM imoveis WHERE id = %s'
    cursor.execute(sql, (imovel_id,))
    
    imovel = cursor.fetchone()
    if not imovel:
        resp = {"erro": "Imóvel não encontrado"}
        return resp, 404
    
    imovel_dict = {
        "id": imovel[0],
                "logradouro": imovel[1],
                "tipo_logradouro": imovel[2],
                "bairro": imovel[3],
                "cidade": imovel[4],
                "cep": imovel[5],
                "tipo": imovel[6],
                "valor": imovel[7],
                "data_aquisicao": imovel[8]
    }
    
    resp = jsonify(imovel_dict)
    return resp, 200

@app.route("/imoveis", methods=['POST'])
def post_imovel():
    conn = connect_db()
    if conn is None:
        resp = {"erro": "Ocorreu um erro ao conectar com o servidor"}
        return resp, 500
    
    cursor = conn.cursor()
    data = request.json
    logradouro = data.get("logradouro")
    tipo_logradouro = data.get("tipo_logradouro")
    bairro = data.get("bairro")
    cidade = data.get("cidade")
    cep = data.get("cep")
    tipo = data.get("tipo")
    valor = data.get("valor")
    data_aquisicao = data.get("data_aquisicao")
    
    if not all([logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao]):
        return {"erro": "Todos os campos são obrigatórios"}, 400
    
    try:
        sql = "INSERT INTO imoveis (logradouro,tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, (
        logradouro,
        tipo_logradouro,
        bairro,
        cidade,
        cep,
        tipo,
        valor,
        data_aquisicao
        ))
        conn.commit()
        return {'mensagem': 'Imóvel adicionado com sucesso'}, 201

    except Exception as e:
        return {"erro": str(e)}, 500
    
@app.route("/imoveis/<int:imovel_id>", methods=['PUT'])
def editar_imovel(imovel_id):
    conn = connect_db()
    if conn is None:
        resp = {"erro": "Ocorreu um erro ao conectar com o servidor"}
        return resp, 500
    
    cursor = conn.cursor()
    sql = "SELECT * FROM imoveis WHERE ID = %s"
    cursor.execute(sql, (imovel_id,))
    
    imovel = cursor.fetchone()
    if not imovel:
        resp = {'erro': 'Imóvel não encontrado'}
        return resp, 404
    
    data = request.json
    logradouro = data.get("logradouro")
    tipo_logradouro = data.get("tipo_logradouro")
    bairro = data.get("bairro")
    cidade = data.get("cidade")
    cep = data.get("cep")
    tipo = data.get("tipo")
    valor = data.get("valor")
    data_aquisicao = data.get("data_aquisicao")
    
    if not all([logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao]):
        return {"erro": "Todos os campos são obrigatórios"}, 400
    
    try:
        sql_update = "UPDATE imoveis SET logradouro = %s, tipo_logradouro = %s, bairro = %s, cidade = %s, cep = %s, tipo = %s, valor = %s, data_aquisicao = %s WHERE id = %s"
        cursor.execute(sql_update, (logradouro,
        tipo_logradouro,
        bairro,
        cidade,
        cep,
        tipo,
        valor,
        data_aquisicao,
        imovel_id))
        conn.commit()
        
        imovel_editado = {
            "id": imovel_id,
            "logradouro": logradouro,
            "tipo_logradouro": tipo_logradouro,
            "bairro": bairro,
            "cidade": cidade,
            "cep": cep,
            "tipo": tipo,
            "valor": valor,
            "data_aquisicao": data_aquisicao
        }
        
        return jsonify({"mensagem": "Imóvel atualizado com sucesso"}), 200
    except Exception as e:
        return {'erro': str(e)}, 500
    
@app.route('/imoveis/<int:imovel_id>', methods=['DELETE'])
def delete_imovel(imovel_id):
    conn = connect_db()
    if conn is None:
        return {'erro': 'Ocorreu um erro ao conectar com o servidor'}, 500
    
    try:
        cursor = conn.cursor()
        sql = "DELETE FROM imoveis WHERE id = %s"
        cursor.execute(sql, (imovel_id,))
        conn.commit()
        
        if cursor.rowcount == 0:
            return {'erro': 'Imóvel não encontrado'}, 404
        
    except Exception as e:
        return {'erro': str(e)}, 500
    
    return {"mensagem": "Imóvel deletado com sucesso"}, 200

@app.route('/imoveis/tipo/<string:tipo>', methods = ['GET'])
def get_imovel_tipo(tipo):
    conn = connect_db()
    if conn is None:
        return {'erro': 'Ocorreu um erro ao conectar com o servidor'}, 500
    

    cursor = conn.cursor()
    sql = "SELECT * FROM imoveis WHERE tipo = %s"
    cursor.execute(sql, (tipo, ))
    
    imoveis_tipo = cursor.fetchall()
    if not imoveis_tipo:
        return {'erro': 'Imóvel não encontrado'}, 404
    
    
    imoveis = []
    for imovel in imoveis_tipo:
        imovel_dict = {
        "id": imovel[0],
        "logradouro": imovel[1],
        "tipo_logradouro": imovel[2],
        "bairro": imovel[3],
        "cidade": imovel[4],
        "cep": imovel[5],
        "tipo": imovel[6],
        "valor": imovel[7],
        "data_aquisicao": imovel[8]
        }
        imoveis.append(imovel_dict)
    return {"imoveis": imoveis}, 200

@app.route('/imoveis/cidade/<string:cidade>', methods = ['GET'])
def get_imovel_cidade(cidade):
    conn = connect_db()
    if conn is None:
        return {'erro': 'Ocorreu um erro ao conectar com o servidor'}, 500
    

    cursor = conn.cursor()
    sql = "SELECT * FROM imoveis WHERE cidade = %s"
    cursor.execute(sql, (cidade, ))
    
    imoveis_tipo = cursor.fetchall()
    if not imoveis_tipo:
        return {'erro': 'Imóvel não encontrado'}, 404
    
    
    imoveis = []
    for imovel in imoveis_tipo:
        imovel_dict = {
        "id": imovel[0],
        "logradouro": imovel[1],
        "tipo_logradouro": imovel[2],
        "bairro": imovel[3],
        "cidade": imovel[4],
        "cep": imovel[5],
        "tipo": imovel[6],
        "valor": imovel[7],
        "data_aquisicao": imovel[8]}
        imoveis.append(imovel_dict)
    return {"imoveis": imoveis}, 200

if __name__ == "__main__":
    app.run(debug=True)