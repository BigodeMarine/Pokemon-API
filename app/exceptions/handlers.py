from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.logging import logger
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.status import (
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_503_SERVICE_UNAVAILABLE,
)

from app.exceptions import (
    PokemonAlreadyExists,
    PokemonNotFound,
    PokeAPIUnavailable,
    ValidationException,
)

"""
Registra todos os handlers globais.
"""
def register_exception_handlers(app: FastAPI):

    @app.exception_handler(PokemonNotFound)
    async def pokemon_not_found(
        request: Request,
        exc: PokemonNotFound,
    ):
        logger.warning(
            "Pokémon não encontrado",
            extra={
            "method": request.method,
            "path": request.url.path,
            "status": 404,
            "exception": "PokemonNotFound",
    },
)
        return JSONResponse(
            status_code=HTTP_404_NOT_FOUND,
            content={
                "detail": exc.message
            },
        )

    @app.exception_handler(PokemonAlreadyExists)
    async def pokemon_exists(
        request: Request,
        exc: PokemonAlreadyExists,
    ):
        logger.warning(
            "Pokémon já cadastrado",
            extra={
            "method": request.method,
            "path": request.url.path,
            "status": 409,
            "exception": "PokemonAlreadyExists",
    },
)
        return JSONResponse(
            status_code=HTTP_409_CONFLICT,
            content={
                "detail": exc.message
            },
        )

    @app.exception_handler(PokeAPIUnavailable)
    async def pokeapi_error(
        request: Request,
        exc: PokeAPIUnavailable,
    ):
        logger.error(
            "Falha ao acessar a PokeAPI",
            extra={
            "method": request.method,
            "path": request.url.path,
            "status": 503,
            "exception": "PokeAPIUnavailable",
    },
)
        return JSONResponse(
            status_code=HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "detail": exc.message
            },
        )

    @app.exception_handler(ValidationException)
    async def validation_error(
        request: Request,
        exc: ValidationException,
    ):
        return JSONResponse(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "detail": exc.message
            },
        )
    app.add_exception_handler(
        Exception,
        internal_server_error_handler,
)

"""
Captura erros inesperados.
"""
async def internal_server_error_handler(
    request: Request,
    exc: Exception,
):
    
    logger.exception(
        "Erro interno da aplicação",
        extra={
            "method": request.method,
            "path": request.url.path,
            "status": 500,
            "exception": exc.__class__.__name__,
        },
    )

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Erro interno do servidor."
        },
    )