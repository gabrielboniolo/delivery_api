from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import pegar_sessao
from main import bcrypt_context

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def auth():
    """ Rota padrão de autenticação do sistema """
    return {"mensagem": "Você acessou a rota de autenticação.", "autenticado": False}

@auth_router.post("/criar_conta")
async def criar_conta(nome:str, email:str, senha:str, session = Depends(pegar_sessao)):
    """ Rota para a criação da conta """

    usuario = session.query(Usuario).filter(Usuario.email==email).first()

    if usuario:
        raise HTTPException(status_code=400, detail="Usuário já cadastrado")
    else:
        senha_criptografada = bcrypt_context.hash(senha)
        novo_usuario = Usuario(nome, email, senha_criptografada)
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": f"Usuário cadastrado com sucesso {email}."}