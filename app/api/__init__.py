from fastapi import APIRouter

from .end_points import folder, file

api_router = APIRouter()
api_router.include_router(folder.router, prefix="/folder", tags=["folder"])
api_router.include_router(file.router, prefix="/file", tags=["file"])
