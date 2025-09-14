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
        (1, "logradouro", "tipo_logradouro", "bairro", "cidade", "cep", "tipo", "valor", "data_aquisicao"),
        (2, "logradouro2", "tipo_logradouro2", "bairro2", "cidade2", "cep2", "tipo2", "valor2", "data_aquisicao2"),
    ]
    }

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