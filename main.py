from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Configuração do aplicativo FastAPI
app = FastAPI(title="Sistema de Gerenciamento de Itens",
              description="Uma API simples para gerenciar itens em um banco de dados.",
              version="1.0.0")

# Conexão com o banco de dados e definições de ORM
DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

# Modelo ORM para os itens
class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)

# Criação das tabelas no banco de dados
Base.metadata.create_all(bind=engine)

@app.post("/items/")
def create_item(name: str):
    """
    Cria um novo item no banco de dados.
    """
    db = SessionLocal()
    new_item = Item(name=name)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

@app.get("/items/{item_id}")
def read_item(item_id: int):
    """
    Retorna um item específico pelo ID.
    """
    db = SessionLocal()
    item = db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/items/{item_id}")
def update_item(item_id: int, name: str):
    """
    Atualiza um item existente pelo ID.
    """
    db = SessionLocal()
    item = db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    item.name = name
    db.commit()
    return item

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    """
    Exclui um item específico pelo ID.
    """
    db = SessionLocal()
    item = db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(item)
    db.commit()
    return {"detail": "Item deleted"}
