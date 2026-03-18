from sqlalchemy import Column, Integer
from app.utils.database import Base

class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)