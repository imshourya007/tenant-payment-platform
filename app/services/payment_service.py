import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import update
from app.models.payment import Payment
from app.models.tenant import Tenant
from app.models.enums import TenantStatus
from app.tasks.refund_tasks import process_refund
from app.tasks.email_task import send_email
from sqlalchemy import select


async def process_payment_webhook(db: AsyncSession, payload):
    try:
        tenant_result = await db.execute(
            select(Tenant).where(Tenant.id == payload.tenant_id)
        )
        tenant = tenant_result.scalar_one()

        payment = Payment(
            id=uuid.uuid4(),
            payment_id=payload.payment_id,
            tenant_id=tenant.id,
            status=payload.status
        )

        db.add(payment)
        await db.flush()

    except IntegrityError:
        # 🔥 Duplicate payment_id case
        await db.rollback()
        return "duplicate_ignored"

    # Conditional activation
    result = await db.execute(
        update(Tenant)
        .where(
            Tenant.id == payload.tenant_id,
            Tenant.status == TenantStatus.PAYMENT_PENDING
        )
        .values(status=TenantStatus.ACTIVE)
    )

    activated = result.rowcount == 1

    await db.commit()

    if activated:
        return "activated"

    process_refund.delay(payload.provider_payment_id)
    send_email.delay(user_email, "Refund Initiated", "...")

    return "already_active_refund_needed"
