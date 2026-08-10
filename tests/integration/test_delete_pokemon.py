"""
Teste para excluir um Pokémon.
"""
def test_delete_pokemon(client):

    create_response = client.post(
        "/pokemons",
        json={
            "pokemon_id": 16
        }
    )

    if create_response.status_code == 201:
        pokemon_id = create_response.json()["id"]

    elif create_response.status_code == 409:
        list_response = client.get("/pokemons")
        assert list_response.status_code == 200

        pokemon = next(
            p for p in list_response.json()["data"]
            if p["pokemon_id"] == 16
        )

        pokemon_id = pokemon["id"]

    else:
        assert False, f"Resposta inesperada: {create_response.status_code}"

    response = client.delete(f"/pokemons/{pokemon_id}")

    assert response.status_code == 204

    response = client.get(f"/pokemons/{pokemon_id}")

    assert response.status_code == 404