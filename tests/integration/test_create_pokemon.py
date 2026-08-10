"""
Teste do cadastro do Pokémon utilizando a PokeAPI.
"""
def test_create_pokemon(client):

    response = client.post(
        "/pokemons",
        json={
            "pokemon_id": 1
        }
    )

    assert response.status_code in (201, 409)

    if response.status_code == 201:
        body = response.json()

        assert body["pokemon_id"] == 1
        assert body["name"] == "bulbasaur"
        assert body["height"] > 0
        assert body["weight"] > 0

        assert "sprites" in body
        assert "types" in body