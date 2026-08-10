from fastapi import Depends
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.repositories.pokemon_repository import PokemonRepository
from app.services.pokemon_service import PokemonService

"""
Cria uma instância do repositório utilizando a sessão atual do banco de dados.
"""
def get_pokemon_repository(
    db: Session = Depends(get_db),
) -> PokemonRepository:
    
    return PokemonRepository(db)

"""
Cria uma instância do serviço de Pokémons. O serviço recebe o repositório já configurado.
"""
def get_pokemon_service(
    repository: PokemonRepository = Depends(get_pokemon_repository),
) -> PokemonService:
    
    return PokemonService(repository)