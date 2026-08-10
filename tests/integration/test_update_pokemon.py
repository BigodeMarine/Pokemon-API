"""
Teste deve atualizar um Pokémon existente.
"""
def test_update_pokemon(client):

    create_response = client.post(
        "/pokemons",
        json={
            "pokemon_id": 10
        }
    )

    if create_response.status_code == 201:
        pokemon_id = create_response.json()["id"]

    elif create_response.status_code == 409:
        list_response = client.get("/pokemons")
        assert list_response.status_code == 200

        pokemon = next(
            p for p in list_response.json()["data"]
            if p["pokemon_id"] == 10
        )

        pokemon_id = pokemon["id"]

    else:
        assert False, f"Resposta inesperada: {create_response.status_code}"

    response = client.put(
        f"/pokemons/{pokemon_id}",
        json={
            "name": "caterpie-updated"
        }
    )

    assert response.status_code == 200

    body = response.json()

    assert body["id"] == pokemon_id
    assert body["name"] == "caterpie-updated"