from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def auth():
    """ Rota padrão de autenticação do sistema """
    return {"mensagem": "Você acessou a rota de autenticação.", "autenticado": False}