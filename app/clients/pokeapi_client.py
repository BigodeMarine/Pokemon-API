from http import HTTPStatus
import httpx
from app.exceptions import PokeAPIUnavailable, PokemonNotFound

"""
Cliente responsável por consumir a PokeAPI.
"""
class PokeAPIClient:
    
    BASE_URL = "https://pokeapi.co/api/v2/pokemon"

    """
    Busca um Pokémon na PokeAPI.
    """
    async def get_pokemon(self, pokemon_id: int) -> dict:

        url = f"{self.BASE_URL}/{pokemon_id}"

        try:
            async with httpx.AsyncClient(timeout=10) as client:

                response = await client.get(url)

        except httpx.RequestError:
            raise PokeAPIUnavailable()

        if response.status_code == HTTPStatus.NOT_FOUND:
            raise PokemonNotFound(pokemon_id)

        if response.status_code != HTTPStatus.OK:
            raise PokeAPIUnavailable()

        return response.json()