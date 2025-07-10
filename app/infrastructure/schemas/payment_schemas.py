from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

from app.core.entities.payment import PaymentStatus


class PaymentCreateInput(BaseModel):
    nombre_cliente: str = Field(..., example="Juan Perez")
    monto: float = Field(..., example=150.75)


class PaymentOutput(BaseModel):
    id: int = Field(..., example=1)
    nombre_cliente: str = Field(..., example="Juan Perez")
    monto: float = Field(..., example=150.75)
    fecha: datetime = Field(..., example="2025-07-08T10:00:00Z")
    estado: PaymentStatus = Field(..., example=PaymentStatus.COMPLETED)
