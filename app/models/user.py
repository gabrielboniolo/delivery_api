from sqlalchemy import Column, String, Boolean
from app.models.base_model import BaseModel

class Usuario(BaseModel):
    __tablename__ = "usuarios"

    nome = Column(String)
    email = Column(String, nullable=False)
    senha = Column(String)
    ativo = Column(Boolean)
    admin = Column(Boolean, default=False)

    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin