from fastapi import APIRouter

from src.api.v1.endpoints import payments

router = APIRouter()
router.include_router(payments.router, prefix="/bot", tags=["bot"])
