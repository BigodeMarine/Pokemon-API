"""
Teste do retorno da lista de Pokémons.
"""
def test_get_pokemons(client):

    response = client.get("/pokemons")

    assert response.status_code == 200

    body = response.json()

    assert "data" in body
    assert "pagination" in body

    assert isinstance(body["data"], list)

    assert "total" in body["pagination"]
    assert "limit" in body["pagination"]
    assert "offset" in body["pagination"]