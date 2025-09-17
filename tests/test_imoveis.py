import pytest
from unittest.mock import patch, MagicMock
from app.routes.servidor import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_conexao_mockada():
    with patch("app.routes.servidor.connect_db") as mock_conn:
        mock_conn.return_value = "fake_conn"
        resp = mock_conn()
        assert resp == "fake_conn"


@patch("app.routes.servidor.connect_db")
def test_get_imoveis(mock_connect_db, client):

    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [
        (1, "logradouro", "tipo_logradouro", "bairro", "cidade", "cep", "tipo", "valor", "data_aquisicao"),
        (2, "logradouro2", "tipo_logradouro2", "bairro2", "cidade2", "cep2", "tipo2", "valor2", "data_aquisicao2"),
    ]

    mock_connect_db.return_value = mock_conn

    response = client.get("/imoveis")

    assert response.status_code == 200
    data = response.get_json()
    
    assert len(data["imoveis"]) == 2

    imovel1 = data["imoveis"][0]
    assert imovel1["id"] == 1
    assert imovel1["logradouro"] == "logradouro"
    assert imovel1["cidade"] == "cidade"
    assert "_links" in imovel1
    assert "self" in imovel1["_links"]
    assert "update" in imovel1["_links"]
    assert "delete" in imovel1["_links"]

    imovel2 = data["imoveis"][1]
    assert imovel2["id"] == 2
    assert imovel2["logradouro"] == "logradouro2"
    assert imovel2["cidade"] == "cidade2"
    assert "_links" in imovel2
    assert "self" in imovel2["_links"]
    assert "update" in imovel2["_links"]
    assert "delete" in imovel2["_links"]

@patch("app.routes.servidor.connect_db")
def test_get_imovel_id(mock_connect_db, client):
    
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    
    mock_cursor.fetchone.return_value = (
        1, "logradouro1", "tipo_logradouro1", "bairro1", "cidade1", "cep1", "tipo1", "valor1", "data_aquisicao1")
    
    mock_connect_db.return_value = mock_conn
    response = client.get("/imoveis/1")
    data = response.get_json()
    
    assert response.status_code == 200
    assert data["id"] == 1
    assert data["logradouro"] == "logradouro1"
    assert data["tipo_logradouro"] == "tipo_logradouro1"
    assert data["bairro"] == "bairro1"
    assert data["cidade"] == "cidade1"
    assert data["cep"] == "cep1"
    assert data["tipo"] == "tipo1"
    assert data["valor"] == "valor1"
    assert data["data_aquisicao"] == "data_aquisicao1"
    assert "_links" in data
    
@patch("app.routes.servidor.connect_db")
def test_imovel_nao_encontrado(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect_db.return_value = mock_conn 
    mock_conn.cursor.return_value = mock_cursor
    
    mock_cursor.fetchone.return_value = None
    response = client.get("/imoveis/1")
    
    assert response.status_code == 404
    assert response.get_json() == {"erro": "Imóvel não encontrado"}
     
@patch("app.routes.servidor.connect_db")
def test_post_imovel(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    
    novo_imovel = {
        "logradouro": "Consolação",
        "tipo_logradouro": "Rua",
        "bairro": "Jardins",
        "cidade": "São Paulo",
        "cep":"01000-000",
        "tipo": "apartamento",
        "valor": "1000000",
        "data_aquisicao":"2024/10/03"
    }
    
    mock_connect_db.return_value = mock_conn
    response = client.post("/imoveis", json=novo_imovel)
    
    assert response.status_code == 201
    assert response.get_json() == {"mensagem": "Imóvel adicionado com sucesso"}
    
@patch("app.routes.servidor.connect_db")
def test_atualizar_imovel(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    imovel_editado = {
        "logradouro": "Consolação",
        "tipo_logradouro": "Rua",
        "bairro": "Jardins",
        "cidade": "São Paulo",
        "cep":"01000-000",
        "tipo": "apartamento",
        "valor": "1000000",
        "data_aquisicao":"2024/10/03",
        "_links": {
                "self": {"href": "http://localhost:5000/imoveis/1", "method": "GET"},
            "update": {"href": "http://localhost:5000/imoveis/1", "method": "PUT"},
            "delete": {"href": "http://localhost:5000/imoveis/1", "method": "DELETE"},
            "all": {"href": "http://localhost:5000/imoveis", "method": "GET"}}}
    
    
    response = client.put("/imoveis/1", json=imovel_editado)
    
    assert response.status_code == 200
    data = response.get_json()
    
    assert "mensagem" in data
    assert data["mensagem"] == "Imóvel atualizado com sucesso"
    assert "imovel" in data
    
    imovel = data["imovel"]
    assert imovel["logradouro"] == "Consolação"
    assert imovel["tipo_logradouro"] == "Rua"
    assert imovel["bairro"] == "Jardins"
    assert imovel["cidade"] == "São Paulo"
    assert imovel["cep"] == "01000-000"
    assert imovel["tipo"] == "apartamento"
    assert imovel["valor"] == "1000000"
    assert imovel["data_aquisicao"] == "2024/10/03"
    assert "_links" in imovel
    
@patch("app.routes.servidor.connect_db")
def test_remover_imovel(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    response = client.delete("/imoveis/1")
    
    assert response.status_code == 200
    assert response.get_json() == {"mensagem": "Imóvel deletado com sucesso"}   
    
@patch("app.routes.servidor.connect_db")
def test_listar_imovel_tipo(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    mock_cursor.fetchall.return_value = [
        (1, "Consolação", "Rua", "Jardins", "São Paulo", "01000-000", "apartamento", "1000000", "2024/10/03"), 
        (2, "Constante Sodré", "Rua", "Praia do Canto", "Espirito Santo", "10000-000", "apartamento", "1000000", "2012/10/03")
                                         ]
    
    response = client.get("/imoveis/tipo/apartamento")
    
    assert response.status_code == 200
    data = response.get_json()
    
    assert "imoveis" in data
    assert len(data["imoveis"]) == 2

    imovel1 = data["imoveis"][0]
    assert imovel1["id"] == 1
    assert imovel1["logradouro"] == "Consolação"
    assert imovel1["bairro"] == "Jardins"
    assert imovel1["cidade"] == "São Paulo"
    assert imovel1["tipo"] == "apartamento"
    assert "_links" in imovel1
    assert "self" in imovel1["_links"]
    assert "update" in imovel1["_links"]
    assert "delete" in imovel1["_links"]

    imovel2 = data["imoveis"][1]
    assert imovel2["id"] == 2
    assert imovel2["logradouro"] == "Constante Sodré"
    assert imovel2["bairro"] == "Praia do Canto"
    assert imovel2["cidade"] == "Espirito Santo"
    assert imovel2["tipo"] == "apartamento"
    assert "_links" in imovel2

@patch("app.routes.servidor.connect_db")
def test_lista_imovel_cidade(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    mock_cursor.fetchall.return_value = [
        (1, "Consolação", "Rua", "Jardins", "São Paulo", "01000-000", "apartamento", "1000000", "2024/10/03")
    ]
    
    response = client.get("/imoveis/cidade/São Paulo")
    
    assert response.status_code == 200
    data = response.get_json()

    assert "imoveis" in data
    assert len(data["imoveis"]) == 1

    imovel = data["imoveis"][0]

    assert imovel["id"] == 1
    assert imovel["logradouro"] == "Consolação"
    assert imovel["tipo_logradouro"] == "Rua"
    assert imovel["bairro"] == "Jardins"
    assert imovel["cidade"] == "São Paulo"
    assert imovel["cep"] == "01000-000"
    assert imovel["tipo"] == "apartamento"
    assert imovel["valor"] == "1000000"
    assert imovel["data_aquisicao"] == "2024/10/03"

    assert "_links" in imovel