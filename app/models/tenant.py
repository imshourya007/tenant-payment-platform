from sqlalchemy import Column, String, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from sqlalchemy import Column, String
from app.db.session import Base
from app.models.enums import TenantStatus

class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    order_id = Column(String, unique=True, nullable=False)

    status = Column(
        Enum(TenantStatus),
        default=TenantStatus.CREATED,
        nullable=False
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())