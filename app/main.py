# app/main.py
import logging
from fastapi import FastAPI
from pyctuator.pyctuator import Pyctuator
import uvicorn
import os

from app.infrastructure.http_handlers.payment_handler import (
    router_payments,
)  # Importar el nuevo router
from app.infrastructure.http_handlers.handler_health_check import router_health

# Configuración básica de logging si no está en log.py de forma global
logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="PayTrack API",
    description="API para el registro, gestión y consulta de pagos realizados por clientes.",
    version="1.0.0",
)

# Integrar Pyctuator para monitoreo (opcional, pero útil para health check)
pyctuator = Pyctuator(
    app=app,
    app_name="PayTrackApp",  # Nombre de tu aplicación
    app_url="http://localhost:8000",  # URL donde se ejecutará tu API
    registration_url=None,  # URL para el registro
    pyctuator_endpoint_url="/pyctuator",  # Este ya lo tenías, lo mantenemos
)


# Registrar routers
app.include_router(router_payments)
app.include_router(router_health)


# Puedes añadir un endpoint raíz simple para verificar que la app corre
@app.get("/")
async def root():
    return {"message": "PayTrack API is running!"}


if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host=host, port=port)
