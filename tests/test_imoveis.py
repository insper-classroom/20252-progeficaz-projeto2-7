import pytest
from unittest.mock import patch, MagicMock
from wsgi import app, connect_db   

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_conexao_mockada():
    with patch("api.connect_db") as mock_conn:
        mock_conn.return_value = "fake_conn"
        resp = connect_db()
        assert resp == "fake_conn"


@patch("wsgi.connect_db")
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
    assert response.get_json() == {
        "imoveis": [
            {"id": 1,
             "logradouro": "logradouro",
             "tipo_logradouro": "tipo_logradouro",
             "bairro": "bairro",
             "cidade": "cidade",
             "cep": "cep",
             "tipo": "tipo",
             "valor": "valor",
             "data_aquisicao": "data_aquisicao",
            },
            {"id": 2,
             "logradouro": "logradouro2",
             "tipo_logradouro": "tipo_logradouro2",
             "bairro": "bairro2",
             "cidade": "cidade2",
             "cep": "cep2",
             "tipo": "tipo2",
             "valor": "valor2",
             "data_aquisicao": "data_aquisicao2",
            }]}

@patch("wsgi.connect_db")
def test_get_imovel_id(mock_connect_db, client):
    
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    
    mock_cursor.fetchone.return_value = (
        1, "logradouro1", "tipo_logradouro1", "bairro1", "cidade1", "cep1", "tipo1", "valor1", "data_aquisicao1")
    
    mock_connect_db.return_value = mock_conn
    response = client.get("/imoveis/1")
    
    assert response.status_code == 200
    assert response.get_json() == {
    "id": 1,
    "logradouro": "logradouro1",
    "tipo_logradouro": "tipo_logradouro1",
    "bairro": "bairro1",
    "cidade": "cidade1",
    "cep": "cep1",
    "tipo": "tipo1",
    "valor": "valor1",
    "data_aquisicao": "data_aquisicao1"
}
    
@patch("wsgi.connect_db")
def test_imovel_nao_encontrado(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect_db.return_value = mock_conn 
    mock_conn.cursor.return_value = mock_cursor
    
    mock_cursor.fetchone.return_value = None
    response = client.get("/imoveis/1")
    
    assert response.status_code == 404
    assert response.get_json() == {"mensagem": "Imóvel não encontrado"}
     
@patch("wsgi.connect_db")
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
        "data_aquisicao":"03/10/2024"
    }
    
    mock_connect_db.return_value = mock_conn
    response = client.post("/imoveis", json=novo_imovel)
    
    assert response.status_code == 201
    assert response.get_json() == {"mensagem": "Imóvel adicionado com sucesso"}
    
@patch("wsgi.connect_db")
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
        "data_aquisicao":"03/10/2024"
    }
    
    response = client.put("/imoveis/1", json=imovel_editado)
    
    assert response.status_code == 200
    assert response.get_json() == {"mensagem": "Imóvel atualizado com sucesso"}  
    
@patch("wsgi.connect_db")
def test_remover_imovel(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    response = client.delete("/imoveis/1")
    
    assert response.status_code == 200
    assert response.get_json() == {"mensagem": "Imóvel deletado com sucesso"}   
    
@patch("wsgi.connect_db")
def test_listar_imovel_tipo(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    mock_cursor.fetchall.return_value = [
        (1, "Consolação", "Rua", "Jardins", "São Paulo", "01000-000", "apartamento", "1000000", "03/10/2024"), 
        (2, "Constante Sodré", "Rua", "Praia do Canto", "Espirito Santo", "10000-000", "apartamento", "1000000", "03/10/2012")
                                         ]
    
    response = client.get("/imoveis/tipo/apartamento")
    
    assert response.status_code == 200
    assert response.get_json() == {"imoveis": [
        { "id": 1,
        "logradouro": "Consolação",
        "tipo_logradouro": "Rua",
        "bairro": "Jardins",
        "cidade": "São Paulo",
        "cep":"01000-000",
        "tipo": "apartamento",
        "valor": "1000000",
        "data_aquisicao":"03/10/2024"},
        { "id": 2,
        "logradouro": "Constante Sodré",
        "tipo_logradouro": "Rua",
        "bairro": "Praia do Canto",
        "cidade": "Espirito Santo",
        "cep":"10000-000",
        "tipo": "apartamento",
        "valor": "1000000",
        "data_aquisicao":"03/10/2012"}
        ]
        }

@patch("wsgi.connect_db")
def test_lista_imovel_cidade(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    mock_cursor.fetchall.return_value = [
        (1, "Consolação", "Rua", "Jardins", "São Paulo", "01000-000", "apartamento", "1000000", "03/10/2024")
    ]
    
    response = client.get("/imoveis/cidade/São Paulo")
    
    assert response.status_code == 200
    assert response.get_json() == {"imoveis":
        [
        { "id": 1,
        "logradouro": "Consolação",
        "tipo_logradouro": "Rua",
        "bairro": "Jardins",
        "cidade": "São Paulo",
        "cep":"01000-000",
        "tipo": "apartamento",
        "valor": "1000000",
        "data_aquisicao":"03/10/2024"}
        ]
        }