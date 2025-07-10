import logging
from datetime import datetime
from typing import List, Optional

from app.core.entities.payment import Payment, PaymentStatus
from app.core.ports.repositories.payment_repository_base import PaymentRepositoryBase
from app.application.payment_service_port import PaymentServiceBase

logger = logging.getLogger(__name__)


class PaymentService(PaymentServiceBase):
    def __init__(self, payment_repository: PaymentRepositoryBase):
        self.payment_repository = payment_repository

    def register_payment(self, nombre_cliente: str, monto: float) -> Optional[Payment]:
        logger.info(
            f"Attempting to register payment for client: {nombre_cliente}, amount: {monto}"
        )
        if monto <= 0:
            logger.warning("Payment amount must be greater than zero.")
            return None

        new_payment = Payment(
            id=None,
            nombre_cliente=nombre_cliente,
            monto=monto,
            fecha=datetime.now(),
            estado=PaymentStatus.COMPLETED,
        )

        saved_payment = self.payment_repository.save(new_payment)
        logger.info(f"Payment registered successfully: {saved_payment.id}")
        return saved_payment

    def list_all_payments(self) -> List[Payment]:
        logger.info("Listing all payments.")
        return self.payment_repository.get_all()

    def search_payments_by_client(self, client_name: str) -> List[Payment]:
        logger.info(f"Searching payments for client: {client_name}")
        return self.payment_repository.get_by_client_name(client_name)

    def delete_payment(self, payment_id: int) -> bool:
        logger.info(f"Attempting to delete payment with ID: {payment_id}")
        payment_to_delete = self.payment_repository.get_by_id(payment_id)
        if not payment_to_delete:
            logger.warning(f"Payment with ID {payment_id} not found for deletion.")
            return False

        if payment_to_delete.estado != PaymentStatus.COMPLETED:
            logger.warning(
                f"Payment with ID {payment_id} cannot be deleted as its status is not COMPLETED."
            )
            return False

        return self.payment_repository.delete(payment_id)
