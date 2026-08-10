from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import JSON
from sqlalchemy import String
from sqlalchemy import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from app.database.base import Base

# Modelo que representa um Pokémon persistido no banco.
class Pokemon(Base):

    __tablename__ = "pokemons"

    # Chave primária interna
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    # ID oficial da PokeAPI
    pokemon_id: Mapped[int] = mapped_column(
        Integer,
        unique=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True
    )

    height: Mapped[int]

    weight: Mapped[int]

    types: Mapped[list] = mapped_column(
        JSON
    )

    front_sprite: Mapped[str]

    back_sprite: Mapped[str]

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )