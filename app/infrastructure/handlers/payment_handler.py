# app/infrastructure/handlers/payment_handler.py
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
    """
    Registrar un nuevo pago. [cite: 21]
    """
    logger.info(
        f"Received request to register payment for client: {payment_input.nombre_cliente}, amount: {payment_input.monto}"
    )

    # RF1: El monto debe ser mayor que cero. [cite: 26] -> Esto ya está validado por Pydantic (gt=0) en PaymentCreateInput,
    # pero el servicio también maneja la regla de negocio.
    registered_payment = payment_service.register_payment(
        nombre_cliente=payment_input.nombre_cliente, monto=payment_input.monto
    )

    if registered_payment is None:
        # RF1: HTTP 400 en caso de error de validación (ej. monto negativo). [cite: 31]
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Monto del pago debe ser mayor que cero.",
        )

    return PaymentOutput(**registered_payment.to_dict())


@router_payments.get("/payments", response_model=List[PaymentOutput])
async def list_all_payments_endpoint(
    request: Request, payment_service: PaymentService = Depends(get_payment_service)
):
    """
    Listar todos los pagos registrados. [cite: 33]
    """
    logger.info("Received request to list all payments.")
    payments = payment_service.list_all_payments()
    # RF2: HTTP 200 con una lista de objetos Pago. [cite: 38]
    return [PaymentOutput(**p.to_dict()) for p in payments]


@router_payments.get(
    "/payments/client/{client_name}", response_model=List[PaymentOutput]
)
async def search_payments_by_client_endpoint(
    request: Request,
    client_name: str,
    payment_service: PaymentService = Depends(get_payment_service),
):
    """
    Consultar todos los pagos realizados por un cliente específico. [cite: 40]
    """
    logger.info(f"Received request to search payments for client: {client_name}")
    payments = payment_service.search_payments_by_client(client_name)
    # RF3: HTTP 200 con lista de pagos encontrados. [cite: 50]
    # RF3: Si no se encuentran pagos, retornar lista vacía. [cite: 48]
    return [PaymentOutput(**p.to_dict()) for p in payments]


@router_payments.delete(
    "/payments/{payment_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_payment_endpoint(
    request: Request,
    payment_id: int,
    payment_service: PaymentService = Depends(get_payment_service),
):
    """
    Eliminar un pago registrado. [cite: 52]
    """
    logger.info(f"Received request to delete payment with ID: {payment_id}")

    deleted = payment_service.delete_payment(payment_id)

    if not deleted:
        # RF4: Si el pago no existe o no puede eliminarse, retornar un mensaje de error. [cite: 56]
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
    # RF4: HTTP 204 en caso de eliminación exitosa. [cite: 58]
    return {}  # No Content
