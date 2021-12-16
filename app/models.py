from sqlalchemy import Column, ForeignKey, String, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID

from .db import Base
from .utils import BaseModelMixin, TimestampMixin, SoftDeleteMixin


class Folder(BaseModelMixin, TimestampMixin, SoftDeleteMixin, Base):
    parent_id = Column(UUID(as_uuid=True), ForeignKey("folder.id"), nullable=True)
    name = Column(String(255))
    path = Column(Text())


class File(BaseModelMixin, TimestampMixin, SoftDeleteMixin, Base):
    name = Column(String(255), nullable=False)
    mime_type = Column(String(255), nullable=False)
    description = Column(String(1024), nullable=True)
    starred = Column(Boolean(), default=False)
    trashed = Column(Boolean(), default=False)
    path = Column(Text())
    folder_id = Column(UUID(as_uuid=True), ForeignKey("folder.id"), nullable=False)
