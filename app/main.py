import logging
from fastapi import FastAPI
import uvicorn
import os

from app.infrastructure.http_handlers.payment_handler import router_payments

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="PayTrack API",
    description="API para gestión de pagos",
    version="1.0.0",
)

app.include_router(router_payments)


@app.get("/")
async def root():
    return {"message": "PayTrack en ejecución"}


if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host=host, port=port)
