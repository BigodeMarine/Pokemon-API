import json
from redis.exceptions import RedisError
from app.cache.redis import redis_client
from app.core.config import settings
from app.core.logging import logger


class PokemonCache:
    """Best-effort cache: PostgreSQL remains the source of truth."""

    TTL = 300

    @staticmethod
    def pokemon_key(pokemon_id: int) -> str:
        return f"pokemon:{pokemon_id}"

    @staticmethod
    def list_key(limit: int, offset: int) -> str:
        return f"pokemons:{limit}:{offset}"

    @staticmethod
    def _unavailable(operation: str, error: Exception):
        # Do not log connection URLs, credentials or cached payloads.
        logger.warning(
            "Redis indisponível; operação de cache ignorada: %s (%s)",
            operation,
            type(error).__name__,
        )

    @staticmethod
    async def get(key: str):
        if not settings.REDIS_ENABLED:
            return None
        try:
            value = await redis_client.get(key)
        except RedisError as error:
            PokemonCache._unavailable("get", error)
            return None
        if value is None:
            return None
        try:
            return json.loads(value)
        except (ValueError, TypeError) as error:
            PokemonCache._unavailable("decode", error)
            return None

    @staticmethod
    async def set(key: str, value):
        if not settings.REDIS_ENABLED:
            return
        payload = json.dumps(value)
        try:
            await redis_client.setex(key, PokemonCache.TTL, payload)
        except RedisError as error:
            PokemonCache._unavailable("set", error)

    @staticmethod
    async def delete(key: str):
        if not settings.REDIS_ENABLED:
            return
        try:
            await redis_client.delete(key)
        except RedisError as error:
            PokemonCache._unavailable("delete", error)

    @staticmethod
    async def clear_lists():
        if not settings.REDIS_ENABLED:
            return
        try:
            keys = await redis_client.keys("pokemons:*")
            if keys:
                await redis_client.delete(*keys)
        except RedisError as error:
            PokemonCache._unavailable("clear_lists", error)
