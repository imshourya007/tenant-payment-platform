from sqlalchemy import Column, String, Enum, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.db.session import Base
from app.models.enums import PaymentStatus


class Payment(Base):
    __tablename__ = "payments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    payment_id = Column(String, unique=True, nullable=False)  # idempotency key from provider
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)

    status = Column(
        Enum(PaymentStatus),
        nullable=False
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())
