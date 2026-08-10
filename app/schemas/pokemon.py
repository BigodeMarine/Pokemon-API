from typing import List
from pydantic import BaseModel, ConfigDict, Field
from app.schemas.pagination import Pagination

"""
Esse schema agrupa os sprites retornados pela PokeAPI para manter a resposta organizada.
"""
class SpriteResponse(BaseModel):

    front_default: str | None = None
    back_default: str | None = None

"""
Dados necessários para cadastrar um Pokémon.
"""
class PokemonCreate(BaseModel):
    
    pokemon_id: int = Field(
        ...,
        gt=0,
        description="ID do Pokémon na PokeAPI."
    )

"""
Dados permitidos para atualização.
"""
class PokemonUpdate(BaseModel):

    name: str | None = None
  
    height: int | None = Field(
        default=None,
        ge=0,
    )

    weight: int | None = Field(
        default=None,
        ge=0,
    )


"""
Esse schema define exatamente quais informações serão enviadas ao cliente.
"""
class PokemonResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int

    pokemon_id: int

    name: str

    height: int

    weight: int

    types: List[str]

    sprites: SpriteResponse

class PokemonListResponse(BaseModel):
    """
    Resposta utilizada no endpoint GET /pokemons.

    Contém a lista de Pokémons juntamente
    com as informações de paginação.
    """

    data: List[PokemonResponse]

    pagination: Pagination

PokemonListResponse.model_rebuild()