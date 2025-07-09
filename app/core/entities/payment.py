from datetime import datetime
from enum import Enum


class PaymentStatus(str, Enum):
    COMPLETED = "COMPLETADO"


class Payment:
    def __init__(
        self,
        id: int,
        nombre_cliente: str,
        monto: float,
        fecha: datetime,
        estado: PaymentStatus,
    ):
        self.id = id
        self.nombre_cliente = nombre_cliente
        self.monto = monto
        self.fecha = fecha
        self.estado = estado

    def to_dict(self):
        return {
            "id": self.id,
            "nombre_cliente": self.nombre_cliente,
            "monto": self.monto,
            "fecha": self.fecha.isoformat(),
            "estado": self.estado.value,
        }
