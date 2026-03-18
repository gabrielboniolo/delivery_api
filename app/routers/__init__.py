from fastapi import FastAPI
from app.routers.auth import auth_router
from app.routers.order import order_router

def include_routers(app: FastAPI):
    app.include_router(auth_router)
    app.include_router(order_router)