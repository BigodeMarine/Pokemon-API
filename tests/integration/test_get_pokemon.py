"""
Teste que deve retornar um Pokémon pelo ID interno.
"""
def test_get_pokemon_by_id(client):

    create_response = client.post(
        "/pokemons",
        json={
            "pokemon_id": 4
        }
    )

    if create_response.status_code == 201:
        pokemon_id = create_response.json()["id"]

    elif create_response.status_code == 409:
        list_response = client.get("/pokemons")
        assert list_response.status_code == 200

        pokemons = list_response.json()["data"]

        pokemon = next(
            p for p in pokemons
            if p["pokemon_id"] == 4
        )

        pokemon_id = pokemon["id"]

    else:
        assert False, f"Resposta inesperada: {create_response.status_code}"

    response = client.get(f"/pokemons/{pokemon_id}")

    assert response.status_code == 200

    body = response.json()

    assert body["pokemon_id"] == 4
    assert body["name"] == "charmander"