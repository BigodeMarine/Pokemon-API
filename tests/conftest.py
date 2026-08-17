import os

os.environ["DATABASE_URL"] = (
    "postgresql+psycopg://postgres:postgres@localhost:5432/pokemon_db"
)

import pytest
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient
from app.main import app
from app.cache.pokemon_cache import PokemonCache


"""
Desabilita o Redis durante os testes.
"""
@pytest.fixture(autouse=True)
def mock_redis():
   
    PokemonCache.get = AsyncMock(return_value=None)
    PokemonCache.set = AsyncMock()
    PokemonCache.delete = AsyncMock()
    PokemonCache.clear_lists = AsyncMock()

"""
Cliente HTTP utilizado pelos testes de integração.
"""
@pytest.fixture
def client():
   
    with TestClient(app) as client:
        yield client