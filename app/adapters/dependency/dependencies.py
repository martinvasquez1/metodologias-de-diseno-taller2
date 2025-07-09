from app.adapters.repositories.in_memory_payment_repository import (
    InMemoryPaymentRepository,
)
from app.application.services.payment_service import PaymentService


in_memory_repo = InMemoryPaymentRepository()


def get_payment_service() -> PaymentService:
    return PaymentService(in_memory_repo)
