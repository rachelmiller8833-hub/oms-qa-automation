from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List
from db import connect_db, get_db
from orders_repo import insert_order, find_order
from bson import ObjectId
from schemas import OrderCreate, OrderUpdate, OrderOut
import orders_repo
import db


app = FastAPI()

@app.on_event("startup")
async def startup():
    await db.connect_db()

@app.on_event("shutdown")
async def shutdown():
    await db.close_db()


class Item(BaseModel):
    product_id: str
    name: str
    price: float
    quantity: int


class OrderCreate(BaseModel):
    user_id: str
    items: List[Item]
    total_price: float
    status: str = "Pending"

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/orders", status_code=201)
async def create_order(order: OrderCreate, db_handle = Depends(get_db)):
    order_id = await orders_repo.insert_order(db_handle, order.model_dump())
    return {"_id": order_id}

@app.get("/orders/{order_id}", response_model=OrderOut, response_model_by_alias=True)
async def get_order(order_id: str, db_handle = Depends(get_db)):
    return await orders_repo.find_order(db_handle,order_id)

@app.put("/orders/{order_id}", response_model=OrderOut, response_model_by_alias=True)
async def update_order_endpoint(order_id: str, payload: OrderUpdate, db=Depends(get_db)):
    updates = payload.model_dump(exclude_none=True)
    return await orders_repo.update_order(db, order_id, updates)


@app.delete("/orders/{order_id}")
async def delete_order_endpoint(order_id: str, db=Depends(get_db)):
    await orders_repo.delete_order(db, order_id)
    return {"status": "deleted"}



