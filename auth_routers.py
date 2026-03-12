from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

from main import bcrypt_context, SECRET_KEY, ALGORITHM, ACESS_TOKEN_EXPIRE_MINUTES
from models import Usuario
from dependencies import pegar_sessao, authorize_token
from schemas import UsuarioSchema, LoginSchema

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def create_token(id_usuario, duracao_token=timedelta(minutes=ACESS_TOKEN_EXPIRE_MINUTES)):
    expiration_date = str(datetime.now(timezone.utc) + duracao_token)
    dict_info = {"sub": str(id_usuario), "expiration_date": expiration_date}
    encoded_jwt = jwt.encode(dict_info, SECRET_KEY, ALGORITHM)
    return encoded_jwt

def authenticate_user(email, password, session):
    user = session.query(Usuario).filter(Usuario.email==email).first()
    if not user:
        return False
    elif not bcrypt_context.verify(password, user.senha):
        return False
    else:
        return user

@auth_router.get("/")
async def auth():
    """ System authentication standard route. """
    return {"mensagem": "Você acessou a rota de autenticação.", "autenticado": False}

@auth_router.post("/criar_conta")
async def criar_conta(usuario_schema:UsuarioSchema, session:Session = Depends(pegar_sessao)):
    """ Create account route. """

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
    """ Login route. """

    login_email = login_schema.email
    login_password = login_schema.senha

    auth_user = authenticate_user(login_email, login_password, session)

    if not auth_user:
        raise HTTPException(status_code=400, detail="Usuário não encontrado")
    else:
        access_token = create_token(auth_user.id)
        refresh_token = create_token(auth_user.id, duracao_token=timedelta(days=7))
        return {
            "acess_token": access_token,
            " refresh_token": refresh_token,
            "token_type": "Bearer"
        }
@auth_router.get("/refresh")
async def use_refresh_token(verified_user_token:Usuario = Depends(authorize_token)):
    access_token = create_token(verified_user_token.id)
    return {
            "acess_token": access_token,
            "token_type": "Bearer"
        }