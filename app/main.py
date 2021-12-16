
from fastapi import FastAPI

from .api import api_router

app = FastAPI()


app = FastAPI(title="ClickSign Storage Service v1")

app.include_router(api_router)
