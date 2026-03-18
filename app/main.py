from fastapi import FastAPI
from app.routers import include_routers

app = FastAPI()
include_routers(app)