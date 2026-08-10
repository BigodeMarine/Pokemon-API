import json
from app.cache.redis import redis_client

"""
Responsável por armazenar e recuperar informações
dos Pokémons no Redis.
"""
class PokemonCache:

    TTL = 300
    """
    Gera a chave utilizada para armazenar um Pokémon individual.
    """
    @staticmethod
    def pokemon_key(pokemon_id: int) -> str:
        
        return f"pokemon:{pokemon_id}"
    """
    Gera a chave para listas paginadas.
    """
    @staticmethod
    def list_key(limit: int, offset: int) -> str:
        
        return f"pokemons:{limit}:{offset}"

    @staticmethod
    async def get(key: str):

        value = await redis_client.get(key)

        if value is None:
            return None

        return json.loads(value)

    @staticmethod
    async def set(key: str, value):

        await redis_client.setex(
            key,
            PokemonCache.TTL,
            json.dumps(value),
        )

    @staticmethod
    async def delete(key: str):

        await redis_client.delete(key)
        
    """
    Remove todos os caches de listagem.
    """
    @staticmethod
    async def clear_lists():
    
        keys = await redis_client.keys("pokemons:*")

        if keys:
            await redis_client.delete(*keys)