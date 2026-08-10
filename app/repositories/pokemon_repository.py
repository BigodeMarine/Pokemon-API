from sqlalchemy.orm import Session
from app.models.pokemon import Pokemon

"""
Responsável por todas as operações de banco relacionadas à Pokemon.
"""
class PokemonRepository:
    
    def __init__(self, db: Session):
        self.db = db

    """
    Salva um novo Pokémon no banco.
    """
    def create(self, pokemon: Pokemon) -> Pokemon:
        
        self.db.add(pokemon)
        self.db.commit()
        self.db.refresh(pokemon)

        return pokemon

    """
    Busca um Pokémon pelo ID.
    """
    def get_by_id(self, pokemon_id: int) -> Pokemon | None:
        
        return (
            self.db.query(Pokemon)
            .filter(Pokemon.id == pokemon_id)
            .first()
        )

    """
    Busca um Pokémon pelo ID da PokeAPI.
    """
    def get_by_pokemon_id(self, pokemon_id: int) -> Pokemon | None:
        
        return (
            self.db.query(Pokemon)
            .filter(Pokemon.pokemon_id == pokemon_id)
            .first()
        )

    """
    Retorna uma lista paginada de Pokémons.
    """
    def get_all(
        self,
        limit: int,
        offset: int,
    ) -> list[Pokemon]:
        
        return (
            self.db.query(Pokemon)
            .order_by(Pokemon.id)
            .offset(offset)
            .limit(limit)
            .all()
        )

    """
    Retorna a quantidade total de Pokémons.
    """
    def count(self) -> int:
        
        return self.db.query(Pokemon).count()

    """
    Persiste alterações realizadas em um Pokémon existente.
    """
    def update(self, pokemon: Pokemon) -> Pokemon:
        
        self.db.commit()
        self.db.refresh(pokemon)

        return pokemon

    """
    Remove um Pokémon do banco.
    """
    def delete(self, pokemon: Pokemon) -> None:
        
        self.db.delete(pokemon)
        self.db.commit()