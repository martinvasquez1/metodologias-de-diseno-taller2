import logging
from typing import List
from fastapi import APIRouter, Request, Depends, HTTPException, status

from app.infrastructure.dependency.dependencies import get_payment_service
from app.infrastructure.schemas.payment_schemas import PaymentCreateInput, PaymentOutput
from app.application.payment_service import PaymentService

logger = logging.getLogger(__name__)
router_payments = APIRouter()


@router_payments.post(
    "/payments", response_model=PaymentOutput, status_code=status.HTTP_201_CREATED
)
async def register_payment_endpoint(
    request: Request,
    payment_input: PaymentCreateInput,
    payment_service: PaymentService = Depends(get_payment_service),
):
    logger.info(
        f"Received request to register payment for client: {payment_input.nombre_cliente}, amount: {payment_input.monto}"
    )

    registered_payment = payment_service.register_payment(
        nombre_cliente=payment_input.nombre_cliente, monto=payment_input.monto
    )

    if registered_payment is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Monto del pago debe ser mayor que cero.",
        )

    return PaymentOutput(**registered_payment.to_dict())


@router_payments.get("/payments", response_model=List[PaymentOutput])
async def list_all_payments_endpoint(
    request: Request, payment_service: PaymentService = Depends(get_payment_service)
):
    logger.info("Received request to list all payments.")
    payments = payment_service.list_all_payments()
    return [PaymentOutput(**p.to_dict()) for p in payments]


@router_payments.get(
    "/payments/client/{client_name}", response_model=List[PaymentOutput]
)
async def search_payments_by_client_endpoint(
    request: Request,
    client_name: str,
    payment_service: PaymentService = Depends(get_payment_service),
):
    logger.info(f"Received request to search payments for client: {client_name}")
    payments = payment_service.search_payments_by_client(client_name)
    return [PaymentOutput(**p.to_dict()) for p in payments]


@router_payments.delete(
    "/payments/{payment_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_payment_endpoint(
    request: Request,
    payment_id: int,
    payment_service: PaymentService = Depends(get_payment_service),
):
    logger.info(f"Received request to delete payment with ID: {payment_id}")

    deleted = payment_service.delete_payment(payment_id)

    if not deleted:
        payment = payment_service.payment_repository.get_by_id(payment_id)
        if not payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pago con ID {payment_id} no encontrado.",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Pago con ID {payment_id} no puede ser eliminado. Estado actual: {payment.estado.value}. Solo se pueden eliminar pagos COMPLETADOS.",
            )
    return {}
