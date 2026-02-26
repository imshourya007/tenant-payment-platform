from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.routes.deps import get_db
from app.schemas.payment import PaymentWebhook
from app.services.payment_service import process_payment_webhook

router = APIRouter()


@router.post("/webhook")
async def payment_webhook(
    payload: PaymentWebhook,
    db: AsyncSession = Depends(get_db),
):
    result = await process_payment_webhook(db, payload)
    return {"result": result}
