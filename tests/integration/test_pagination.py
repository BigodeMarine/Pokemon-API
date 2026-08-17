"""
Testes de paginação da lista de Pokémons.
"""


def test_pagination_limit(client):
    """
    Verifica se o parâmetro limit controla a quantidade de registros.
    """

    response = client.get("/pokemons?limit=2&offset=0")

    assert response.status_code == 200

    body = response.json()

    assert body["pagination"]["limit"] == 2
    assert body["pagination"]["offset"] == 0

    assert len(body["data"]) <= 2


def test_pagination_offset(client):
    """
    Verifica se o parâmetro offset altera a posição inicial da paginação.
    """

    response = client.get("/pokemons?limit=2&offset=2")

    assert response.status_code == 200

    body = response.json()

    assert body["pagination"]["limit"] == 2
    assert body["pagination"]["offset"] == 2


def test_pagination_next(client):
    """
    Verifica se a URL da próxima página é gerada corretamente.
    """

    response = client.get("/pokemons?limit=2&offset=0")

    assert response.status_code == 200

    body = response.json()

    if body["pagination"]["total"] > 2:
        assert body["pagination"]["next"] == "/pokemons?limit=2&offset=2"


def test_pagination_previous(client):
    """
    Verifica se a URL da página anterior é gerada corretamente.
    """

    response = client.get("/pokemons?limit=2&offset=2")

    assert response.status_code == 200

    body = response.json()

    if body["pagination"]["total"] > 2:
        assert body["pagination"]["previous"] == "/pokemons?limit=2&offset=0"