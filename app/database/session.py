from collections.abc import Generator
from urllib.parse import urlparse
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from app.core.config import settings

"""
A Engine representa a conexão principal com o banco de dados.
"""

db_url = urlparse(settings.DATABASE_URL)

print(
    "DATABASE DEBUG:",
    {
        "host": db_url.hostname,
        "port": db_url.port,
        "database": db_url.path,
        "scheme": db_url.scheme,
    },
)

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
)

"""
Cada requisição da API receberá sua própria sessão.
"""
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)

"""
Cria uma sessão do banco para a requisição atual.
"""
def get_db() -> Generator[Session, None, None]:

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()