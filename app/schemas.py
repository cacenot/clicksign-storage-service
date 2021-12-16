from typing import Optional
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel
from pydantic.types import constr


class FolderBase(BaseModel):
    parent_id: UUID
    name: str


class FolderCreate(FolderBase):
    name: constr(regex=r'^[^\\/?%*:|"<>\.]+$', min_length=1, max_length=255)


class FolderUpdate(FolderBase):
    name: Optional[constr(regex=r'^[^\\/?%*:|"<>\.]+$', min_length=1, max_length=255)]
    parent_id: Optional[UUID]


class Folder(FolderBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class RootFolder(Folder):
    parent_id: Optional[UUID]


class FileBase(BaseModel):
    description: Optional[str]
    starred: Optional[bool]
    trashed: Optional[bool]
    folder_id: UUID


class FileUpdate(FileBase):
    name: Optional[constr(regex=r'^[^\\/?%*:|"<>\.]+$', min_length=1, max_length=255)]
    description: Optional[constr(min_length=1, max_length=1024)]
    folder_id: Optional[UUID]


class File(FileBase):
    id: UUID
    name: str
    mime_type: str
    created_at: datetime
    updated_at: Optional[datetime]
    folder_id: UUID

    class Config:
        orm_mode = True
