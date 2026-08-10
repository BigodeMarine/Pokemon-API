import pytest
from unittest.mock import AsyncMock, MagicMock
from app.schemas.pokemon import PokemonCreate
from app.services.pokemon_service import PokemonService
from unittest.mock import patch
from app.models.pokemon import Pokemon
from app.exceptions import PokemonAlreadyExists
from app.exceptions import PokeAPIUnavailable

"""
Testes Unitários do Service
"""
@pytest.mark.asyncio
async def test_create_pokemon_success():

    repository = MagicMock()

    service = PokemonService(repository)

    repository.get_by_pokemon_id.return_value = None

    service.client.get_pokemon = AsyncMock(
        return_value={
            "id": 25,
            "name": "pikachu",
            "height": 4,
            "weight": 60,
            "types": [
                {
                    "type": {
                        "name": "electric"
                    }
                }
            ],
            "sprites": {
                "front_default": "front.png",
                "back_default": "back.png",
            },
        }
    )

    pokemon = Pokemon(
        pokemon_id=25,
        name="pikachu",
        height=4,
        weight=60,
        types=["electric"],
        front_sprite="front.png",
        back_sprite="back.png",
)

    pokemon.id = 1

    repository.create.return_value = pokemon

    with patch(
        "app.services.pokemon_service.PokemonCache.clear_lists",
        new_callable=AsyncMock,
):
        response = await service.create(
            PokemonCreate(
                pokemon_id=25
        )
    )

    assert response.name == "pikachu"
    assert response.pokemon_id == 25
    assert response.types == ["electric"]

    repository.create.assert_called_once()

"""
Esse teste verifica se o serviço impede o cadastro duplicado.
"""
@pytest.mark.asyncio
async def test_create_existing_pokemon():

    repository = MagicMock()

    service = PokemonService(repository)

    repository.get_by_pokemon_id.return_value = Pokemon(
        pokemon_id=25,
        name="pikachu",
        height=4,
        weight=60,
        types=["electric"],
        front_sprite="front.png",
        back_sprite="back.png",
    )

    with pytest.raises(PokemonAlreadyExists):
        await service.create(
            PokemonCreate(pokemon_id=25)
        )
"""
Esse teste garante que, se a PokeAPI falhar, o serviço propaga corretamente a exceção.
"""
@pytest.mark.asyncio
async def test_create_when_pokeapi_is_unavailable():

    repository = MagicMock()

    service = PokemonService(repository)

    repository.get_by_pokemon_id.return_value = None

    service.client.get_pokemon = AsyncMock(
        side_effect=PokeAPIUnavailable()
    )

    with pytest.raises(PokeAPIUnavailable):
        await service.create(
            PokemonCreate(
                pokemon_id=25
            )
        )