from pydantic import BaseModel, EmailStr
from uuid import UUID


class TenantCreate(BaseModel):
    email: EmailStr


class TenantResponse(BaseModel):
    id: UUID
    email: EmailStr
    status: str
    order_id: str

    class Config:
        from_attributes = True
