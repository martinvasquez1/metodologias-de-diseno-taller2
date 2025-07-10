# app/infrastructure/http_handlers/handler_health_check.py
import logging
from fastapi import APIRouter, Request

logger = logging.getLogger(__name__)
router_health = APIRouter()


@router_health.get("/pyctuator/health", response_model=None)
async def health_check(request: Request):
    return {"status": "OK", "message": "healthy"}
