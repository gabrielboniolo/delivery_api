from fastapi import Depends
from sqlalchemy.orm import Session, sessionmaker

from models import db, Usuario

def pegar_sessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()

# Preciso importar o Depends porque ele tem que executar a sessão sozinho (chamada dentro do refresh).
def authorize_token(token, session:Session = Depends(pegar_sessao)): 
    # Falta tratar o token passado como parâmetro

    authorized_user = session.query(Usuario).filter(Usuario.id==4)

    return authorized_user 