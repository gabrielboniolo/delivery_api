from fastapi import APIRouter
from models import Usuario, db
from sqlalchemy.orm import sessionmaker

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def auth():
    """ Rota padrão de autenticação do sistema """
    return {"mensagem": "Você acessou a rota de autenticação.", "autenticado": False}

@auth_router.post("/criar_conta")
async def criar_conta(nome:str, email:str, senha:str):
    Session = sessionmaker(bind=db)
    session = Session()
    usuario = session.query(Usuario).filter(Usuario.email==email).first()

    if usuario:
        return {"mensagem": "Já existe um usuário com esse email."}
    else:
        novo_usuario = Usuario(nome, email, senha)
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": "Usuário adicionado com sucesso."}