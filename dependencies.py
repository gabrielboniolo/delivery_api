from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session, sessionmaker
from jose import jwt, JWTError

from main import SECRET_KEY, ALGORITHM, oauth2_schema
from models import db, Usuario

def pegar_sessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()

def authorize_token(token:str = Depends(oauth2_schema), session:Session = Depends(pegar_sessao)):
    try:
        dict_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        user_id = int(dict_info.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Acesso Negado, verifique a validade do token.")

    authorized_user = session.query(Usuario).filter(Usuario.id==user_id).first()

    if not authorized_user:
        raise HTTPException(status_code=401, detail="Acesso Negado, usuário não autorizado.")

    return authorized_user