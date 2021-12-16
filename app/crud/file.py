from typing import Dict, Optional

from fastapi import UploadFile
from pydantic.types import constr
from sqlalchemy.orm import Session

from app.crud.utils import get_folder_path

from ..models import File


def get_file(db: Session, file_id: str):
    return db.query(File).filter(File.id == file_id, File.deleted == False).first() # noqa


def upload_file(
    db: Session,
    folder_id: str,
    description: Optional[constr(min_length=1, max_length=1024)],
    file: UploadFile
):
    path = get_folder_path(db, folder_id)
    db_file = File(
        folder_id=folder_id,
        description=description,
        name=file.filename,
        mime_type=file.content_type,
        path=path
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file


def update_file(db: Session, db_file: File, file: Dict):
    for field in file:
        setattr(db_file, field, file[field])

    if "folder_id" in file:
        file_path = get_folder_path(db, file["parent_id"])
        path = "{}{}".format(file_path, db_file.name)
        setattr(db_file, "path", path)

    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file


def delete_file(db: Session, file_id: str):
    db_file = db.query(File).filter_by(id=file_id).first()
    db_file.delete()
    db.add(db_file)
    db.commit()
