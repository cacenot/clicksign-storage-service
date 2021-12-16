from typing import Dict

from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import or_

from .. import schemas
from ..models import Folder, File
from .utils import get_folder_path


def get_folder(db: Session, folder_id: str):
    return db.query(Folder).filter(Folder.id == folder_id, Folder.deleted == False).first() # noqa


def get_root_folder(db: Session):
    return db.query(Folder).filter(Folder.parent_id == None).first() # noqa


def get_child_folders(db: Session, parent_id: str, skip: int = 0, limit: int = 100):
    return db.query(Folder).filter(Folder.parent_id == parent_id, Folder.deleted == False).offset(skip).limit(limit).all() # noqa


def create_folder(db: Session, folder: schemas.FolderCreate):
    path = get_folder_path(db, folder.parent_id)
    db_folder = Folder(parent_id=folder.parent_id, name=folder.name, path=path)
    db.add(db_folder)
    db.commit()
    db.refresh(db_folder)
    return db_folder


def update_folder(db: Session, db_folder: Folder, folder: Dict):
    for field in folder:
        setattr(db_folder, field, folder[field])

    if "parent_id" in folder:
        path = get_folder_path(db, folder["parent_id"])
        setattr(db_folder, "path", path)

    db.add(db_folder)
    db.commit()
    db.refresh(db_folder)
    return db_folder


def delete_folder(db: Session, folder_id: str):
    db_folders = db.query(Folder).filter(or_(Folder.id == folder_id, Folder.parent_id == folder_id), Folder.deleted == False).all() # noqa

    for db_folder in db_folders:
        db_folder.delete()

    child_files = db.query(File).filter_by(folder_id=folder_id, deleted=False).all()

    for child_file in child_files:
        child_file.delete()

    db.bulk_save_objects(db_folders)
    db.bulk_save_objects(child_files)
    db.commit()
    return [file.id for file in child_files]
