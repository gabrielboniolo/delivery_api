from fastapi import APIRouter

order_router = APIRouter(prefix="/order", tags=["order"])

@order_router.get("/")
async def order():
    """
      Rota padrão de pedidos.
      Todas as rotas e pedidos precisam de autenticação.

    """
    return {"mensagem": "Você acessou a rota de pedidos."}