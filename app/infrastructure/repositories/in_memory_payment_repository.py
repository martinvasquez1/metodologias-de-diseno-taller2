import logging
from typing import List, Optional

from app.core.entities.payment import Payment, PaymentStatus
from app.core.ports.repositories.payment_repository_base import PaymentRepositoryBase

logger = logging.getLogger(__name__)


class InMemoryPaymentRepository(PaymentRepositoryBase):
    def __init__(self):
        self.payments: List[Payment] = []
        self._next_id = 1

    def save(self, payment: Payment) -> Payment:
        if payment.id is None:
            payment.id = self._next_id
            self._next_id += 1

        existing_index = next(
            (i for i, p in enumerate(self.payments) if p.id == payment.id), -1
        )
        if existing_index != -1:
            self.payments[existing_index] = payment
            logger.info(f"Updated payment with ID: {payment.id}")
        else:
            self.payments.append(payment)
            logger.info(f"Saved new payment with ID: {payment.id}")
        return payment

    def get_all(self) -> List[Payment]:
        logger.info("Retrieving all payments from in-memory repository.")
        return list(self.payments)

    def get_by_client_name(self, client_name: str) -> List[Payment]:
        logger.info(
            f"Retrieving payments for client '{client_name}' from in-memory repository."
        )
        return [
            p for p in self.payments if p.nombre_cliente.lower() == client_name.lower()
        ]

    def get_by_id(self, payment_id: int) -> Optional[Payment]:
        logger.info(
            f"Retrieving payment with ID {payment_id} from in-memory repository."
        )
        return next((p for p in self.payments if p.id == payment_id), None)

    def delete(self, payment_id: int) -> bool:
        logger.info(
            f"Attempting to delete payment with ID {payment_id} from in-memory repository."
        )
        initial_len = len(self.payments)
        self.payments = [p for p in self.payments if p.id != payment_id]
        return len(self.payments) < initial_len
