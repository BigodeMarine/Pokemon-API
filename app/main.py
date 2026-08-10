from fastapi import FastAPI
from app.exceptions.handlers import register_exception_handlers
from app.api import pokemon_router
from contextlib import asynccontextmanager
from app.cache.redis import redis_client
from app.middleware.logging import LoggingMiddleware

"""
Executado quando a aplicação inicia.
"""
@asynccontextmanager
async def lifespan(app: FastAPI):

    await redis_client.ping()

    print("✅ Redis conectado com sucesso!")

    yield

    await redis_client.close()

"""
Ponto de entrada da aplicação.
"""
app = FastAPI(
    title="Pokemon API",
    version="1.0.0",
    description="API REST para gerenciamento de Pokémons."
)

app.add_middleware(LoggingMiddleware)

register_exception_handlers(app)

app.include_router(pokemon_router)

"""
Endpoint utilizado para verificar se a aplicação está funcionando.
"""
@app.get("/", tags=["Health"])
async def health():
   
    return {
        "status": "running",
        "message": "Pokemon API iniciada com sucesso!"
    }