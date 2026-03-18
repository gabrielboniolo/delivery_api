from sqlalchemy.orm import declarative_base, Column, Integer
from app.utils.database import Base

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)