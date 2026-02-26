import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.tenant import Tenant
from app.models.enums import TenantStatus


async def create_tenant(db: AsyncSession, email: str):
    # Check duplicate email
    result = await db.execute(select(Tenant).where(Tenant.email == email))
    existing = result.scalar_one_or_none()

    if existing:
        raise ValueError("Tenant already exists")

    # Generate order_id
    order_id = f"order_{uuid.uuid4().hex[:12]}"

    tenant = Tenant(
        id=uuid.uuid4(),
        email=email,
        order_id=order_id,
        status=TenantStatus.PAYMENT_PENDING
    )

    db.add(tenant)
    await db.flush()  # get tenant.id without committing

    await db.commit()
    await db.refresh(tenant)

    return tenant, order_id
