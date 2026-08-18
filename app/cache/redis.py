import redis.asyncio as redis
from app.core.config import settings

"""
Gerencia a conexão com o Redis.
"""
if settings.REDIS_URL:
    redis_client = redis.from_url(
        settings.REDIS_URL,
        decode_responses=True,
    )
else:
    redis_client = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        password=settings.REDIS_PASSWORD or None,
        decode_responses=True,
    )