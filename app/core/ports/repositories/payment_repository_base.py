from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import date

from app.core.entities.payment import Payment, PaymentStatus


class PaymentRepositoryBase(ABC):
    @abstractmethod
    def save(self, payment: Payment) -> Payment:
        pass

    @abstractmethod
    def get_all(self) -> List[Payment]:
        pass

    @abstractmethod
    def get_by_client_name(self, client_name: str) -> List[Payment]:
        pass

    @abstractmethod
    def get_by_id(self, payment_id: int) -> Optional[Payment]:
        pass

    @abstractmethod
    def delete(self, payment_id: int) -> bool:
        pass
