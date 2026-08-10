import redis.asyncio as redis
from app.core.config import settings

"""
Gerencia a conexão com o Redis.
"""
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True,
)