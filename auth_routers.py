from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Usuario
from dependencies import pegar_sessao
from main import bcrypt_context
from schemas import UsuarioSchema, LoginSchema

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def criar_token(id_usuario):
    token = f"ahj53us64bduy5345abs{id_usuario}"
    return token

# def autenticar_usuario(email, senha, session):
#     usuario = session.query(Usuario).filter(Usuario.email==email).first()
#     if not usuario:
#         return False
#     elif not bcrypt_context.verify(senha, usuario.senha):
#         return False
#     else:
#         return usuario

@auth_router.get("/")
async def auth():
    """ Rota padrão de autenticação do sistema """
    return {"mensagem": "Você acessou a rota de autenticação.", "autenticado": False}

@auth_router.post("/criar_conta")
async def criar_conta(usuario_schema:UsuarioSchema, session:Session = Depends(pegar_sessao)):
    """ 
    Rota para a criação da conta 

    """

    verify_user = session.query(Usuario).filter(Usuario.email==usuario_schema.email).first()

    if verify_user:
        raise HTTPException(status_code=400, detail="Usuário já cadastrado")
    else:
        account_name = usuario_schema.nome
        account_email = usuario_schema.email
        account_password = usuario_schema.senha

        crypto_password = bcrypt_context.hash(account_password)

        new_user = Usuario(account_name, account_email, crypto_password)

        session.add(new_user)
        session.commit()
        return {"mensagem": f"Usuário cadastrado com sucesso {account_email}."}
    
@auth_router.post("/login")
async def login(login_schema:LoginSchema, session:Session = Depends(pegar_sessao)):

    login_email = login_schema.email
    login_password = login_schema.senha

    auth_user = session.query(Usuario).filter(Usuario.email==login_email).first()
    # auth_user = autenticar_usuario(login_email, login_password, session)

    if not auth_user:
        raise HTTPException(status_code=400, detail="Usuário não encontrado")
    else:
        access_token = criar_token(auth_user.id)
        return {
            "acess_token": access_token,
            "token_type": "Bearer"
        }