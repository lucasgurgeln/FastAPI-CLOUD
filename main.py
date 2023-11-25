from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text
import os

app = FastAPI()

# Conexão com o banco de dados
DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL)

@app.post("/items/")
def create_item(name: str):
    with engine.connect() as conn:
        result = conn.execute(text("INSERT INTO items (name) VALUES (:name)"), {"name": name})
        conn.commit()
    return {"name": name}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM items WHERE id = :item_id"), {"item_id": item_id})
        item = result.fetchone()
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
    return {"name": item['name']}

@app.put("/items/{item_id}")
def update_item(item_id: int, name: str):
    with engine.connect() as conn:
        conn.execute(text("UPDATE items SET name = :name WHERE id = :item_id"), {"name": name, "item_id": item_id})
        conn.commit()
    return {"name": name}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM items WHERE id = :item_id"), {"item_id": item_id})
        conn.commit()
    return {"detail": "Item deleted"}
