from sqlalchemy.orm import Column, String, Integer, Float, ForeignKey
from base_model import BaseModel

class Pedido(BaseModel):
    __tablename__ = "pedidos"

    status = Column(String)
    usuario = Column(ForeignKey("usuarios.id"))
    preco = Column(Float)

    def __init__(self, usuario, status="pendente", preco=0):
        self.status = status
        self.usuario = usuario
        self.preco = preco

class ItemPedido(BaseModel):
    __tablename__ = "itens_pedido"

    quantidade = Column(Integer)
    sabor = Column(String)
    tamanho = Column(String)
    preco_unitario = Column(Float)
    pedido = Column(ForeignKey("pedidos.id"))

    def __init__(self, quantidade, sabor, tamanho, preco_unitario, pedido):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.pedido = pedido