def formata_imovel(dados):
    """Transforma a tupla do banco em dicionário."""
    return {
        "id": dados[0],
        "logradouro": dados[1],
        "tipo_logradouro": dados[2],
        "bairro": dados[3],
        "cidade": dados[4],
        "cep": str(dados[5]),
        "tipo": dados[6],
        "valor": float(dados[7]),
        "data_aquisicao": str(dados[8])
    }
