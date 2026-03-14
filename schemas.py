from pydantic import BaseModel, ConfigDict
from typing import Optional

class UsuarioSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    nome: str 
    email: str
    senha: str
    ativo: Optional[bool]
    admin: Optional[bool]

    # class Config:
    #     from_attributes = True

class PedidoSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_usuario: int


class LoginSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: str
    senha: str