from sqlalchemy import Column, String, Enum, ForeignKey, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.db.session import Base
from app.models.enums import ProvisioningStatus


class ProvisioningTask(Base):
    __tablename__ = "provisioning_tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)

    task_name = Column(String, nullable=False)

    status = Column(
        Enum(ProvisioningStatus),
        default=ProvisioningStatus.NOT_STARTED,
        nullable=False
    )

    retry_count = Column(Integer, default=0)
    last_error = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
