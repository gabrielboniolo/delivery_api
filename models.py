from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float
from sqlalchemy.orm import declarative_base

db = create_engine("sqlite:///banco.db")
Base = declarative_base

class Usuario(Base):
    __table_name__ = "usuarios"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String)
    email = Column("email", String, nullable=False)
    senha = Column("senha", String)
    ativo = Column("ativo", Boolean)
    admin = Column("admin", Boolean, default=False)

    def __init__(self, nome, email, senha, ativo, admin):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.addmin = admin