from app.cache.pokemon_cache import PokemonCache
from app.models.pokemon import Pokemon
from app.repositories.pokemon_repository import PokemonRepository
from app.schemas.pokemon import (
    PokemonCreate,
    PokemonUpdate,
    PokemonResponse,
    SpriteResponse,
)
from app.exceptions import (
    PokemonAlreadyExists,
    PokemonNotFound,
)
from app.clients import PokeAPIClient

"""
Contém toda a regra de negócio relacionada aos Pokémons.
"""
class PokemonService:

    def __init__(self, repository: PokemonRepository):
        self.repository = repository
        self.client = PokeAPIClient()

    """
    Cadastra um Pokémon consultando a PokeAPI.
    """
    async def create(self, data: PokemonCreate):

        existing = self.repository.get_by_pokemon_id(data.pokemon_id)

        if existing:
            raise PokemonAlreadyExists(data.pokemon_id)

        pokemon_data = await self.client.get_pokemon(data.pokemon_id)

        pokemon = Pokemon(
            pokemon_id=pokemon_data["id"],
            name=pokemon_data["name"],
            height=pokemon_data["height"],
            weight=pokemon_data["weight"],
            types=[
                item["type"]["name"]
                for item in pokemon_data["types"]
            ],
            front_sprite=pokemon_data["sprites"]["front_default"],
            back_sprite=pokemon_data["sprites"]["back_default"],
        )

        created = self.repository.create(pokemon)

        await PokemonCache.clear_lists()

        return self._to_response(created)
    
    """
    Retorna um Pokémon utilizando cache.
    """
    async def get_by_id(self, id: int):
    

        cache_key = PokemonCache.pokemon_key(id)

        cached = await PokemonCache.get(cache_key)

        if cached:

            print("🟢 Redis HIT")

            return cached

        print("🔴 Redis MISS")

        pokemon = self.repository.get_by_id(id)

        if not pokemon:
            raise PokemonNotFound(id)

        response = self._to_response(pokemon)

        await PokemonCache.set(
        cache_key,
        response.model_dump(),
    )

        return response
    
    """
    Retorna uma lista paginada utilizando cache.
    """
    async def get_all(self, limit: int, offset: int):

        cache_key = PokemonCache.list_key(limit, offset)

        cached = await PokemonCache.get(cache_key)

        if cached:

            print("🟢 Redis LIST HIT")

            return cached

        print("🔴 Redis LIST MISS")

        pokemons = self.repository.get_all(limit, offset)
        total = self.repository.count()

        next_url = None
        previous_url = None

        if offset + limit < total:
            next_url = (
                f"/pokemons?limit={limit}&offset={offset + limit}"
        )

        if offset > 0:
            previous_offset = max(0, offset - limit)
            previous_url = (
            f"/pokemons?limit={limit}&offset={previous_offset}"
        )

        response = {
            "data": [
                self._to_response(pokemon).model_dump()
                for pokemon in pokemons
        ],
        "pagination": {
            "total": total,
            "limit": limit,
            "offset": offset,
            "next": next_url,
            "previous": previous_url,
        },
    }

        await PokemonCache.set(cache_key, response)

        return response

    """
    Atualiza um Pokémon.
    """
    async def update(
        self,
        pokemon_id: int,
        data: PokemonUpdate,
    ):

        pokemon = self.repository.get_by_id(pokemon_id)

        if not pokemon:
            raise PokemonNotFound(pokemon_id)

        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(pokemon, field, value)

        updated = self.repository.update(pokemon)

        await PokemonCache.delete(
            PokemonCache.pokemon_key(updated.id)
)

        await PokemonCache.clear_lists()

        return self._to_response(updated)

    """
    Remove um Pokémon.
    """
    async def delete(self, id: int):

        pokemon = self.repository.get_by_id(id)

        if not pokemon:
            raise PokemonNotFound(id)

        self.repository.delete(pokemon)
        await PokemonCache.delete(
            PokemonCache.pokemon_key(id)
)

        await PokemonCache.clear_lists()

        return True

    """
    Converte o Model do SQLAlchemy para o schema da API.
    """
    def _to_response(self, pokemon):
        

        return PokemonResponse(
            id=pokemon.id,
            pokemon_id=pokemon.pokemon_id,
            name=pokemon.name,
            height=pokemon.height,
            weight=pokemon.weight,
            types=pokemon.types,
            sprites=SpriteResponse(
                front_default=pokemon.front_sprite,
                back_default=pokemon.back_sprite,
            ),
        )