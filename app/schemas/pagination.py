from pydantic import BaseModel

"""
Informações de paginação da resposta.
"""
class Pagination(BaseModel):

    total: int
    limit: int
    offset: int
    next: str | None = None
    previous: str | None = None