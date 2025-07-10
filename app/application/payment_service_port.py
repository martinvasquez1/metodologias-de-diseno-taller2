from abc import ABC, abstractmethod
from typing import List, Optional

from app.core.entities.payment import Payment, PaymentStatus


class PaymentServiceBase(ABC):
    @abstractmethod
    def register_payment(self, nombre_cliente: str, monto: float) -> Optional[Payment]:
        pass

    @abstractmethod
    def list_all_payments(self) -> List[Payment]:
        pass

    @abstractmethod
    def search_payments_by_client(self, client_name: str) -> List[Payment]:
        pass

    @abstractmethod
    def delete_payment(self, payment_id: int) -> bool:
        pass
