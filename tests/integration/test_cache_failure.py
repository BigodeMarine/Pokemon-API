"""Exercise real cache methods despite the repository's autouse cache mocks."""
from unittest.mock import AsyncMock
import pytest
from redis.exceptions import ConnectionError, TimeoutError
from app.cache.pokemon_cache import PokemonCache
from app.cache.redis import redis_client
from app.core.config import settings

# Capture implementations at collection time, before conftest replaces them.
GET = PokemonCache.get
SET = PokemonCache.set
DELETE = PokemonCache.delete
CLEAR = PokemonCache.clear_lists


@pytest.mark.asyncio
@pytest.mark.parametrize('error', [ConnectionError('DNS unavailable'), TimeoutError('timeout')])
async def test_cache_outage_is_optional(monkeypatch, error):
    monkeypatch.setattr(settings, 'REDIS_ENABLED', True)
    for method in ['get', 'setex', 'delete', 'keys']:
        monkeypatch.setattr(redis_client, method, AsyncMock(side_effect=error))
    assert await GET('pokemon:1') is None
    await SET('pokemon:1', {'id': 1})
    await DELETE('pokemon:1')
    await CLEAR()


@pytest.mark.asyncio
async def test_disabled_cache_never_connects(monkeypatch):
    monkeypatch.setattr(settings, 'REDIS_ENABLED', False)
    mocks = []
    for method in ['get', 'setex', 'delete', 'keys']:
        mock = AsyncMock(side_effect=AssertionError('Redis must not be called'))
        monkeypatch.setattr(redis_client, method, mock)
        mocks.append(mock)
    assert await GET('pokemon:1') is None
    await SET('pokemon:1', {'id': 1})
    await DELETE('pokemon:1')
    await CLEAR()
    for mock in mocks:
        mock.assert_not_awaited()


def test_get_and_post_survive_redis_outage(client, monkeypatch):
    from app.clients.pokeapi_client import PokeAPIClient
    from app.database.session import SessionLocal
    from app.models.pokemon import Pokemon
    fixture_id = 999998
    with SessionLocal() as db:
        assert db.query(Pokemon).filter_by(pokemon_id=fixture_id).first() is None
    for name, implementation in [('get', GET), ('set', SET), ('delete', DELETE), ('clear_lists', CLEAR)]:
        monkeypatch.setattr(PokemonCache, name, staticmethod(implementation))
    monkeypatch.setattr(settings, 'REDIS_ENABLED', True)
    for method in ['get', 'setex', 'delete', 'keys']:
        monkeypatch.setattr(redis_client, method, AsyncMock(side_effect=ConnectionError('DNS unavailable')))
    monkeypatch.setattr(PokeAPIClient, 'get_pokemon', AsyncMock(return_value={
        'id': fixture_id, 'name': 'cache-outage-test', 'height': 4, 'weight': 60,
        'types': [{'type': {'name': 'electric'}}],
        'sprites': {'front_default': 'https://example.com/front.png', 'back_default': 'https://example.com/back.png'},
    }))
    internal_id = None
    try:
        response = client.post('/pokemons', json={'name': 'cache-outage-test'})
        assert response.status_code == 201, response.text
        internal_id = response.json()['id']
        assert client.get(f'/pokemons/{internal_id}').status_code == 200
        assert client.get('/pokemons').status_code == 200
        assert client.post('/pokemons', json={'pokemon_id': fixture_id}).status_code == 409
    finally:
        if internal_id is not None:
            assert client.delete(f'/pokemons/{internal_id}').status_code == 204
