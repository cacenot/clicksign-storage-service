import os
import shutil
from pathlib import Path

from fastapi import UploadFile

from .config import settings


class StorageService:
    def save_file(self, file_id: str, upload_file: UploadFile):
        path = Path(f"{settings.FILES_ROOT_PATH}/{file_id}")
        with path.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
        upload_file.file.close()

    def delete_file(self, file_id: str):
        os.remove(f"{settings.FILES_ROOT_PATH}/{file_id}")


storage_service = StorageService()
