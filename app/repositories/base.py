from sqlalchemy.orm import Session

"""
Classe base para todos os repositórios.
"""
class BaseRepository:
    
    def __init__(self, db: Session):
       
        self.db = db