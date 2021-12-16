from typing import List, Union

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..deps import get_db
from ...models import Folder
from ... import schemas
from ...crud import folder as crud
from ...storage_service import storage_service


router = APIRouter()


@router.get("/root/", response_model=schemas.RootFolder)
def read_root_folder(db: Session = Depends(get_db)):
    return crud.get_root_folder(db)


@router.post("/", response_model=schemas.Folder)
def create_folder(folder: schemas.FolderCreate, db: Session = Depends(get_db)):
    return crud.create_folder(db, folder=folder)


@router.get("/{folder_id}", response_model=Union[schemas.Folder, schemas.RootFolder])
def read_folder(folder_id: str, db: Session = Depends(get_db)):
    folder = crud.get_folder(db, folder_id)

    if not folder:
        raise HTTPException(status_code=404, detail="Folder not found")

    return folder


@router.put("/{folder_id}", response_model=schemas.Folder)
def update_folder(folder_id: str, folder: schemas.FolderCreate, db: Session = Depends(get_db)):
    db_folder = db.query(Folder).get(folder_id)

    if not db_folder:
        raise HTTPException(status_code=404, detail="Folder not found")

    return crud.update_folder(db, db_folder, folder.dict())


@router.patch("/{folder_id}", response_model=schemas.Folder)
def partial_update_folder(folder_id: str, folder: schemas.FolderUpdate, db: Session = Depends(get_db)):
    db_folder = db.query(Folder).get(folder_id)

    if not db_folder:
        raise HTTPException(status_code=404, detail="Folder not found")

    update_data = folder.dict(exclude_unset=True)
    return crud.update_folder(db, db_folder, update_data)


@router.get("/items/{parent_id}", response_model=List[schemas.Folder])
def read_child_folders(parent_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_child_folders(db, parent_id, skip, limit)


@router.delete("/{folder_id}", response_model=str)
def delete_folder(folder_id: str, db: Session = Depends(get_db)):
    db_folder = crud.get_folder(db, folder_id)

    if not db_folder:
        raise HTTPException(status_code=404, detail="Folder not found")

    child_files = crud.delete_folder(db, folder_id)

    for file_id in child_files:
        storage_service.delete_file(file_id)

    return folder_id
