import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import utils

# Carrega variáveis do arquivo .cred
load_dotenv(".cred")

db_config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME", "imoveis"),
    "port": int(os.getenv("DB_PORT")),
    "ssl_ca": os.getenv("SSL_CA_PATH")
}

def get_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Erro na conexão: {e}")
    return None

# ---------------- FUNÇÕES CRUD ----------------

def listar_imoveis():
    conn = get_connection()
    if not conn:
        return {"erro": "Falha ao conectar ao banco"}, 500
    
    cur = conn.cursor()
    cur.execute("SELECT * FROM imoveis")
    registros = cur.fetchall()

    if not registros:
        return {"erro": "Nenhum imóvel encontrado"}, 404
    
    imoveis = [utils.formata_imovel(item) for item in registros]
    return imoveis, 200


def obter_imovel(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM imoveis WHERE id = %s", (id,))
    registro = cur.fetchone()

    if not registro:
        return {"erro": f"Imóvel {id} não encontrado"}, 404
    
    return utils.formata_imovel(registro), 200


def cadastrar_imovel(imovel):
    conn = get_connection()
    cur = conn.cursor()

    sql = """
        INSERT INTO imoveis (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """
    cur.execute(sql, (
        imovel["logradouro"],
        imovel["tipo_logradouro"],
        imovel["bairro"],
        imovel["cidade"],
        imovel["cep"],
        imovel["tipo"],
        imovel["valor"],
        imovel["data_aquisicao"]
    ))
    conn.commit()

    novo_id = cur.lastrowid
    cur.execute("SELECT * FROM imoveis WHERE id = %s", (novo_id,))
    registro = cur.fetchone()

    if not registro:
        return {"erro": "Erro ao criar imóvel"}, 500
    
    return utils.formata_imovel(registro), 201


def atualizar_imovel(id, imovel):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM imoveis WHERE id = %s", (id,))
    if not cur.fetchone():
        return {"erro": f"Imóvel {id} não encontrado"}, 404

    sql = """
        UPDATE imoveis
        SET logradouro=%s, tipo_logradouro=%s, bairro=%s, cidade=%s,
            cep=%s, tipo=%s, valor=%s, data_aquisicao=%s
        WHERE id=%s
    """
    cur.execute(sql, (
        imovel["logradouro"],
        imovel["tipo_logradouro"],
        imovel["bairro"],
        imovel["cidade"],
        imovel["cep"],
        imovel["tipo"],
        imovel["valor"],
        imovel["data_aquisicao"],
        id
    ))
    conn.commit()

    cur.execute("SELECT * FROM imoveis WHERE id = %s", (id,))
    registro = cur.fetchone()
    return utils.formata_imovel(registro), 200


def excluir_imovel(id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM imoveis WHERE id = %s", (id,))
    if not cur.fetchone():
        return {"erro": f"Imóvel {id} não encontrado"}, 404

    cur.execute("DELETE FROM imoveis WHERE id = %s", (id,))
    conn.commit()
    return {"mensagem": f"Imóvel {id} removido com sucesso"}, 200


def buscar_por_tipo(tipo):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM imoveis WHERE tipo = %s", (tipo,))
    registros = cur.fetchall()

    if not registros:
        return {"erro": "Nenhum imóvel encontrado"}, 404
    
    imoveis = [utils.formata_imovel(item) for item in registros]
    return imoveis, 200


def buscar_por_cidade(cidade):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM imoveis WHERE cidade = %s", (cidade,))
    registros = cur.fetchall()

    if not registros:
        return {"erro": "Nenhum imóvel encontrado"}, 404
    
    imoveis = [utils.formata_imovel(item) for item in registros]
    return imoveis, 200
