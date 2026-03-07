from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

# Code smell! Isn't a good practice to import the main script.
# I have to create a new one for this crypto instance.
from main import bcrypt_context, SECRET_KEY, ALGORITHM, ACESS_TOKEN_EXPIRE_MINUTES
from models import Usuario
from dependencies import pegar_sessao, authorize_token
from schemas import UsuarioSchema, LoginSchema

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def create_token(id_usuario, duracao_token=timedelta(minutes=ACESS_TOKEN_EXPIRE_MINUTES)):
    expiration_date = str(datetime.now(timezone.utc) + duracao_token)
    dict_info = {"sub": id_usuario, "expiration_date": expiration_date}
    encoded_jwt = jwt.encode(dict_info, SECRET_KEY, ALGORITHM)
    return encoded_jwt

# Isn't possible to call a session  beacause that func isn't a route
# Depends() is a function from fastapi module
# Remember that have a problem to call the session on the refresh route
# So it's to throw this function to dependencies script
#
# def verify_token(token, session:Session = Depends(pegar_sessao)): 
#     # Falta validar o token passado como parâmetro
#     find_user = session.query(Usuario).filter(Usuario.id == 1).first()
#     return find_user

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
    """ 
    Create account route. 
    
    usuario_schema: Objeto instanciado a partir de um Schema. Ele só pode ser tratado como
    objeto aqui no código, por conta da classe Config dentro do Schema.

    Se não houvesse essa configuração, na classe Config, só seria possível tratar o Schema
    como um dicionário e não como um objeto.
    Exemplo: name = user_schema["name"] x name = user_schema.name

    Dentro do Swagger, ele interpreta esse parâmetro do tipo Schema e é retornado um dicionário
    formatado com chaves (ao invés de inputs relacionados aos parâmetros da rota), referente aos
    atributos que foram declarados na "ClasseSchema".
    É como se o Pydantic alterasse a forma se instancia um objeto.
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

"""
Dúvidas:

1.1) Token de acesso X Token de refresh (30' e 7 dias, mas como isso afeta o login do usuário).
Eu entendi que após o do refresh, será necessário logar novamente. Mas porque utilizar o "acess token"?

# RESPOSTA: Se um hacker tiver acesso ao acess_token

1.2) Então porque o hacker não acessa o refresh token, já que tem uma duração maior?

# RESPOSTA: O refresh token transita pela rede quando o acess_token expira. Resumindo, ele tem uma
visibilidade menor do que o acess_token, sendo muito mais difícil de acessá-lo.

2) Para que preciso chamar o refresh token como rota?

# RESPOSTA: Gerar um novo acess_token, que expira a cada 30 minutos.


"""