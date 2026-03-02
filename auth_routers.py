from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import pegar_sessao
from main import bcrypt_context
from schemas import UsuarioSchema

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def auth():
    """ Rota padrão de autenticação do sistema """
    return {"mensagem": "Você acessou a rota de autenticação.", "autenticado": False}

@auth_router.post("/criar_conta")
async def criar_conta(usuario_schema:UsuarioSchema, session = Depends(pegar_sessao)):
    """ 
    Rota para a criação da conta 

    """

    usuario = session.query(Usuario).filter(Usuario.email==usuario_schema.email).first()

    if usuario:
        raise HTTPException(status_code=400, detail="Usuário já cadastrado")
    else:
        nome = usuario_schema.nome
        email = usuario_schema.email
        senha = usuario_schema.senha

        senha_criptografada = bcrypt_context.hash(senha)

        novo_usuario = Usuario(nome, email, senha_criptografada)

        session.add(novo_usuario)
        session.commit()
        return {"mensagem": f"Usuário cadastrado com sucesso {email}."}