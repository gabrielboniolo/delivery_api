from typing import Optional
from base_schema import BaseSchema

class UsuarioSchema(BaseSchema):
    nome: str 
    email: str
    senha: str
    ativo: Optional[bool]
    admin: Optional[bool]

class LoginSchema(BaseSchema):
    email: str
    senha: str