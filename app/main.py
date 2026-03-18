from fastapi import FastAPI

app = FastAPI()

from routers.auth import auth_router
from routers.order import order_router

app.include_router(auth_router)
app.include_router(order_router)