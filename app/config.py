import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str
    FILES_ROOT_PATH: str = f"{os.path.abspath(os.path.dirname(__file__))}/files"


settings = Settings()
