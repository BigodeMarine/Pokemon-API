import logging
import sys
from pathlib import Path
from app.core.json_logger import JsonFormatter

"""
Configuração central do logger.
"""
Path("logs").mkdir(exist_ok=True)

logger = logging.getLogger("pokemon-api")

logger.setLevel(logging.INFO)

logger.handlers.clear()

"""
Handler para o terminal
"""
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(JsonFormatter())

"""
Handler para arquivo
"""
file_handler = logging.FileHandler(
    "logs/app.log",
    encoding="utf-8",
)

file_handler.setFormatter(JsonFormatter())

logger.addHandler(console_handler)
logger.addHandler(file_handler)

logger.propagate = False