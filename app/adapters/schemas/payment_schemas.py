# app/adapters/schemas/payment_schemas.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

from app.core.entities.payment import PaymentStatus


# RF1: Entradas para Registrar un Pago [cite: 22]
class PaymentCreateInput(BaseModel):
    nombre_cliente: str = Field(..., example="Juan Perez")
    monto: float = Field(..., example=150.75)  # RF1: Monto > 0 [cite: 26]


# Salida para Pagos (RF1, RF2, RF3)
class PaymentOutput(BaseModel):
    id: int = Field(..., example=1)
    nombre_cliente: str = Field(..., example="Juan Perez")
    monto: float = Field(..., example=150.75)
    fecha: datetime = Field(..., example="2025-07-08T10:00:00Z")
    estado: PaymentStatus = Field(..., example=PaymentStatus.COMPLETED)
