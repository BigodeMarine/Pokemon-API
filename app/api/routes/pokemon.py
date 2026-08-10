from fastapi import APIRouter, Depends, Query, status
from app.dependencies import get_pokemon_service
from app.schemas.pokemon import (
    PokemonCreate,
    PokemonUpdate,
)
from app.services.pokemon_service import PokemonService

router = APIRouter(
    prefix="/pokemons",
    tags=["Pokémons"],
)

"""
Cadastra um Pokémon utilizando seu ID da PokeAPI.
"""
@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar Pokémon"
)
async def create_pokemon(
    data: PokemonCreate,
    service: PokemonService = Depends(get_pokemon_service),
):
   
    return await service.create(data)

"""
Retorna uma lista paginada de Pokémons.
"""
@router.get(
    "",
    summary="Listar Pokémons"
)
async def get_pokemons(
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
        description="Quantidade máxima de registros."
    ),
    offset: int = Query(
        default=0,
        ge=0,
        description="Posição inicial."
    ),
    service: PokemonService = Depends(get_pokemon_service),
):

    return await service.get_all(
        limit=limit,
        offset=offset,
    )

"""
Busca um Pokémon pelo ID interno.
"""
@router.get(
    "/{id}",
    summary="Buscar Pokémon"
)
async def get_pokemon(
    id: int,
    service: PokemonService = Depends(get_pokemon_service),
):
    
    return await service.get_by_id(id)

"""
Atualiza um Pokémon.
"""
@router.put(
    "/{id}",
    summary="Atualizar Pokémon"
)
async def update_pokemon(
    id: int,
    data: PokemonUpdate,
    service: PokemonService = Depends(get_pokemon_service),
):
    
    return await service.update(
        id,
        data,
    )

"""
Remove um Pokémon do banco.
"""
@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir Pokémon"
)
async def delete_pokemon(
    id: int,
    service: PokemonService = Depends(get_pokemon_service),
):

    await service.delete(id)

    return None