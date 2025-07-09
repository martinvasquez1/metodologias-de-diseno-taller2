import logging
from datetime import datetime
from typing import List, Optional

from app.core.entities.payment import Payment, PaymentStatus
from app.core.ports.repositories.payment_repository_base import PaymentRepositoryBase

logger = logging.getLogger(__name__)


class PaymentService:
    def __init__(self, payment_repository: PaymentRepositoryBase):
        self.payment_repository = payment_repository
        # ELIMINAR: self.next_id = 1  # ¡Esta línea es la que causaba el reinicio del ID!

    def register_payment(self, nombre_cliente: str, monto: float) -> Optional[Payment]:
        logger.info(
            f"Attempting to register payment for client: {nombre_cliente}, amount: {monto}"
        )
        if monto <= 0:  # RF1: El monto debe ser mayor que cero.
            logger.warning("Payment amount must be greater than zero.")
            return None  # O lanzar una excepción específica

        # RF1: La fecha se asigna automáticamente al momento del registro.
        # RF1: El estado inicial del pago será "COMPLETADO".
        # IMPORTANTE: NO ASIGNAMOS EL ID AQUÍ. El repositorio lo hará.
        new_payment = Payment(
            id=None,  # Pasamos None para que el repositorio asigne el ID
            nombre_cliente=nombre_cliente,
            monto=monto,
            fecha=datetime.now(),
            estado=PaymentStatus.COMPLETED,
        )
        # ELIMINAR: self.next_id += 1  # Ya no es necesario aquí

        saved_payment = self.payment_repository.save(
            new_payment
        )  # El repositorio devolverá el Payment con el ID asignado
        logger.info(f"Payment registered successfully: {saved_payment.id}")
        return saved_payment

    def list_all_payments(self) -> List[Payment]:
        logger.info("Listing all payments.")
        # RF2: Los pagos se pueden retornar en el orden en que fueron registrados.
        return self.payment_repository.get_all()

    def search_payments_by_client(self, client_name: str) -> List[Payment]:
        logger.info(f"Searching payments for client: {client_name}")
        # RF3: La búsqueda debe ser exacta (opcionalmente insensible a mayúsculas/minúsculas).
        # RF3: Si no se encuentran pagos, retornar lista vacía.
        return self.payment_repository.get_by_client_name(client_name)

    def delete_payment(self, payment_id: int) -> bool:
        logger.info(f"Attempting to delete payment with ID: {payment_id}")
        payment_to_delete = self.payment_repository.get_by_id(payment_id)
        if not payment_to_delete:
            logger.warning(f"Payment with ID {payment_id} not found for deletion.")
            return False  # RF4: Si el pago no existe, retornar un mensaje de error.

        # RF4: Solo puede eliminarse si el estado del pago es "COMPLETADO".
        if payment_to_delete.estado != PaymentStatus.COMPLETED:
            logger.warning(
                f"Payment with ID {payment_id} cannot be deleted as its status is not COMPLETED."
            )
            return False  # RF4: Si no puede eliminarse, retornar un mensaje de error.

        return self.payment_repository.delete(payment_id)
