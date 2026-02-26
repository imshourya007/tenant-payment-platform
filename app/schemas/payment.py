from pydantic import BaseModel
from uuid import UUID


class PaymentWebhook(BaseModel):
    payment_id: str
    tenant_id: UUID
    status: str
