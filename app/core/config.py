from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
"""
Representa todas as configurações da aplicação.
"""
class Settings(BaseSettings):

    APP_NAME: str
    APP_VERSION: str
    APP_DESCRIPTION: str

    DEBUG: bool

    HOST: str
    PORT: int

    DATABASE_URL: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    REDIS_PASSWORD: str = ""
    REDIS_URL: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )

#  lru_cache impede que o arquivo .env seja lido diversas vezes durante a execução.
@lru_cache
def get_settings() -> Settings:
 
    return Settings()


settings = get_settings()