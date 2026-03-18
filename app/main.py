from fastapi import FastAPI
from app.routers.__init__ import include_routers

app = FastAPI()
include_routers(app)