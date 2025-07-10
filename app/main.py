# app/main.py
import logging
from fastapi import FastAPI
import uvicorn
import os

from app.infrastructure.http_handlers.payment_handler import (
    router_payments,
)  # Importar el nuevo router

# Configuración básica de logging si no está en log.py de forma global
logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="PayTrack API",
    description="API para el registro, gestión y consulta de pagos realizados por clientes.",
    version="1.0.0",
)

# Registrar routers
app.include_router(router_payments)


# Puedes añadir un endpoint raíz simple para verificar que la app corre
@app.get("/")
async def root():
    return {"message": "PayTrack API is running!"}


if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host=host, port=port)
