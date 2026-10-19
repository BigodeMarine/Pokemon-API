"""Deterministic registration tests; external HTTPS is mocked, persistence is real."""
from unittest.mock import AsyncMock, patch
import pytest
from app.schemas.pokemon import PokemonCreate
from pydantic import ValidationError
from app.clients.pokeapi_client import PokeAPIClient
import httpx

@pytest.mark.parametrize("payload", [{}, {"name": " "}, {"name": "../pikachu"}, {"name": "pikachu", "pokemon_id": 25}, {"pokemon_id": 0}])
def test_invalid_identifier(payload):
    with pytest.raises(ValidationError):
        PokemonCreate(**payload)


def test_name_registration_and_retrieval(client):
    from app.database.session import SessionLocal
    from app.models.pokemon import Pokemon
    # Reserved fixture ID, removed on completion; no dependency on live PokeAPI.
    fixture_id = 999999
    with SessionLocal() as db:
        assert db.query(Pokemon).filter_by(pokemon_id=fixture_id).first() is None
    data = {"id": fixture_id, "name": "pokedex-test", "height": 4, "weight": 60,
            "types": [{"type": {"name": "electric"}}],
            "sprites": {"front_default": "https://raw.githubusercontent.com/front.png",
                        "back_default": "https://raw.githubusercontent.com/back.png"}}
    internal_id = None
    try:
        with patch.object(PokeAPIClient, 'get_pokemon', new_callable=AsyncMock, return_value=data) as upstream:
            response = client.post('/pokemons', json={"name": "  POKEDEX-TEST  "})
            assert response.status_code == 201, response.text
            pokemon = response.json()
            internal_id = pokemon['id']
            upstream.assert_awaited_once_with('pokedex-test')
            assert pokemon['pokemon_id'] == fixture_id
            assert pokemon['sprites']['front_default'] == data['sprites']['front_default']
            assert pokemon['sprites']['back_default'] == data['sprites']['back_default']
            assert client.get(f'/pokemons/{internal_id}').json() == pokemon
            assert any(p['id'] == internal_id for p in client.get('/pokemons?limit=100').json()['data'])
            assert client.post('/pokemons', json={"name": "pokedex-test"}).status_code == 409
            assert client.post('/pokemons', json={"pokemon_id": fixture_id}).status_code == 409
    finally:
        if internal_id is not None:
            assert client.delete(f'/pokemons/{internal_id}').status_code == 204

@pytest.mark.asyncio
async def test_client_queries_upstream_by_name():
    response = httpx.Response(200, json={"id":25}, request=httpx.Request('GET', 'https://pokeapi.co/api/v2/pokemon/pikachu'))
    with patch('app.clients.pokeapi_client.httpx.AsyncClient') as factory:
        upstream = factory.return_value.__aenter__.return_value
        upstream.get = AsyncMock(return_value=response)
        assert await PokeAPIClient().get_pokemon('pikachu') == {"id":25}
        upstream.get.assert_awaited_once_with('https://pokeapi.co/api/v2/pokemon/pikachu')


def test_frontend_assets(client):
    page = client.get('/pokedex')
    assert page.status_code == 200
    assert 'text/html' in page.headers['content-type']
    assert 'id="search-form"' in page.text
    assert client.get('/static/pokedex.js').status_code == 200
    assert client.get('/static/pokedex.css').status_code == 200
    assert client.get('/').json()['status'] == 'running'
