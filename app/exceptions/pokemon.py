"""
Classe base para todas as exceções da aplicação.
"""
class PokemonException(Exception):
    pass

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

"""
Lançada quando o Pokémon já está cadastrado no banco de dados.
"""
class PokemonAlreadyExists(PokemonException):

    def __init__(self, pokemon_id: int):
        super().__init__(
            f"O Pokémon com ID {pokemon_id} já está cadastrado."
        )

"""
Lançada quando um Pokémon não é encontrado.
"""
class PokemonNotFound(PokemonException):

    def __init__(self, pokemon_id: int):
        super().__init__(
            f"Pokémon com ID {pokemon_id} não encontrado."
        )

"""
Lançada quando a PokeAPI não puder ser acessada.
"""
class PokeAPIUnavailable(PokemonException):

    def __init__(self):
        super().__init__(
            "A PokeAPI está indisponível no momento."
        )

"""
Erro de validação da regra de negócio.
"""
class ValidationException(PokemonException):
    
    def __init__(self, message: str):
        super().__init__(message)