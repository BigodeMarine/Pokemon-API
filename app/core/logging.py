import logging
import os
import sys
from pathlib import Path

from app.core.json_logger import JsonFormatter


"""
Configuração central do logger.

Em ambientes locais/Docker:
- escreve logs no terminal;
- escreve logs em logs/app.log.

Na Vercel:
- escreve logs somente no stdout;
- não tenta criar arquivos ou diretórios,
  pois o filesystem da Function é somente leitura.
"""


logger = logging.getLogger("pokemon-api")

logger.setLevel(logging.INFO)

# Evita handlers duplicados caso o módulo seja carregado novamente.
logger.handlers.clear()


"""
Esse handler funciona tanto localmente quanto na Vercel.
A Vercel captura o stdout e disponibiliza os logs no painel.
"""

console_handler = logging.StreamHandler(sys.stdout)

console_handler.setFormatter(JsonFormatter())

logger.addHandler(console_handler)


"""
Detecta se a aplicação está rodando na Vercel.
"""

is_vercel = os.getenv("VERCEL") == "1"


"""
Na Vercel não criamos:
    logs/
    logs/app.log
"""

if not is_vercel:
    log_directory = Path("logs")
    log_directory.mkdir(exist_ok=True)

    file_handler = logging.FileHandler(
        log_directory / "app.log",
        encoding="utf-8",
    )

    file_handler.setFormatter(JsonFormatter())

    logger.addHandler(file_handler)


logger.propagate = False