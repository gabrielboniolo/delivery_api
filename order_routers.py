from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import pegar_sessao
from schemas import PedidoSchema
from models import Pedido

order_router = APIRouter(prefix="/pedidos", tags=["pedidos"])

@order_router.get("/")
async def pedidos():
  """
  Rota padrão de pedidos.
  Todas as rotas e pedidos precisam de autenticação.

  """
  return {"mensagem": "Você acessou a rota de pedidos."}

@order_router.post("/pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session : Session  = Depends(pegar_sessao)):
  """  
  Rota para a criação de pedidos.
    
  """

  novo_pedido = Pedido(usuario=pedido_schema.id_usuario)

  session.add(novo_pedido)
  session.commit()

  return {"mensagem": f"O pedido foi criado com sucesso. ID do pedido: {novo_pedido.id}"}