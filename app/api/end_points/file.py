from typing import Optional

from fastapi import APIRouter, Depends, UploadFile, Form, HTTPException, File as ApiFile
from sqlalchemy.orm import Session
from starlette.responses import FileResponse

from ..deps import get_db
from ...config import settings
from ... import schemas
from ...crud import file as crud
from ...models import File
from ...storage_service import storage_service


router = APIRouter()


@router.post("/upload", response_model=schemas.File)
def upload_file(
    folder_id: str = Form(...),
    description: Optional[str] = Form(...),
    file: UploadFile = ApiFile(...),
    db: Session = Depends(get_db)
):
    db_file = crud.upload_file(db, folder_id, description, file)
    storage_service.save_file(db_file.id, file)
    return db_file


@router.get("/{file_id}", response_model=schemas.File)
def read_file(file_id: str, db: Session = Depends(get_db)):
    file = crud.get_file(db, file_id)

    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    return file


@router.patch("/{file_id}", response_model=schemas.File)
def partial_update_file(file_id: str, file: schemas.FileUpdate, db: Session = Depends(get_db)):
    db_file = db.query(File).get(file_id)

    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")

    update_data = file.dict(exclude_unset=True)
    return crud.update_file(db, db_file, update_data)


@router.delete("/{file_id}", response_model=str)
def delete_file(file_id: str, db: Session = Depends(get_db)):
    db_file = crud.get_file(db, file_id)

    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")

    storage_service.delete_file(db_file.id)
    crud.delete_file(db, file_id)
    return file_id


@router.get("/download/{file_id}")
def download_file(file_id: str, db: Session = Depends(get_db)):
    db_file = crud.get_file(db, file_id)

    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")

    path = f"{settings.FILES_ROOT_PATH}/{db_file.id}"
    return FileResponse(path=path, media_type=db_file.mime_type, filename=db_file.name)
