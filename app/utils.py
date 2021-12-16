from uuid import uuid4
from sqlalchemy import Boolean, Column, DateTime, func
from sqlalchemy.orm import declarative_mixin, declared_attr
from sqlalchemy.dialects.postgresql import UUID


@declarative_mixin
class BaseModelMixin:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)


@declarative_mixin
class TimestampMixin:
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


@declarative_mixin
class SoftDeleteMixin:
    deleted = Column(Boolean, default=False)

    def delete(self):
        self.deleted = True
