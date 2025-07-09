# app/utils/log.py
import logging
import uuid

# from fastapi import Request # No es necesario para la configuración básica del logger

# Configuración del logger
logging.basicConfig(
    level=logging.INFO,  # Nivel de logging global
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],  # Envía logs a la consola
)

logger = logging.getLogger(__name__)
