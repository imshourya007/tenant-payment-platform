from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.routes.deps import get_db
from app.schemas.tenant import TenantCreate, TenantResponse
from app.services.tenant_service import create_tenant

router = APIRouter()


@router.post("", response_model=TenantResponse)
async def create_new_tenant(
    payload: TenantCreate,
    db: AsyncSession = Depends(get_db),
):
    try:
        tenant, order_id = await create_tenant(db, payload.email)
    except ValueError:
        raise HTTPException(status_code=409, detail="Tenant already exists")

    return {
        "id": tenant.id,
        "email": tenant.email,
        "status": tenant.status,
        "order_id": order_id,
    }
