from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException, Depends, Request
from pydantic import BaseModel, Field
from typing import List
from db import connect_db, get_db
from orders_repo import insert_order, find_order
from bson import ObjectId
from schemas import OrderCreate, OrderUpdate, OrderOut
import os
from payment_client import PaymentClient, PaymentResult
import orders_repo
import db


app = FastAPI()

# Initialize database connection on application startup
@app.on_event("startup")
async def startup():
    await db.connect_db()

# Close database connection on application shutdown
@app.on_event("shutdown")
async def shutdown():
    await db.close_db()

class FakePaymentClient:
    # Lightweight mock used for tests to simulate payment success/failure
    def charge(self, user_id: str, amount: float, should_fail: bool = False) -> PaymentResult:
        should_fail = os.getenv("PAYMENT_SHOULD_FAIL", "0") == "1"
        if should_fail:
            return PaymentResult(ok=False, error="mock_failure")
        return PaymentResult(ok=True)


def get_payment_client():
    # Dependency that switches between real and mock payment client via env var
    mode = os.getenv("PAYMENT_MODE", "real")  # real | mock
    if mode == "mock":
        return FakePaymentClient()
    return PaymentClient()

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/orders", status_code=201)
async def create_order(
    order: OrderCreate, 
    request: Request,
    db_handle = Depends(get_db),
    payment_client: PaymentClient = Depends(get_payment_client),
):
    # Optional header-based failure to support negative payment test scenarios
    if request.headers.get("X-Payment-Fail") == "1":
        raise HTTPException(status_code=402, detail="Payment failed")

    payment_result = payment_client.charge(
        order.user_id,
        order.total_price,
        request.headers.get("X-Payment-Fail") == "1"
    )
    if not payment_result.ok:
        raise HTTPException(status_code=402, detail="Payment failed")

    order_id = await orders_repo.insert_order(db_handle, order.model_dump())
    return {"_id": order_id}

@app.get("/orders/{order_id}", response_model=OrderOut, response_model_by_alias=True)
async def get_order(order_id: str, db_handle = Depends(get_db)):
    return await orders_repo.find_order(db_handle, order_id)

@app.put("/orders/{order_id}", response_model=OrderOut, response_model_by_alias=True)
async def update_order_endpoint(order_id: str, payload: OrderUpdate, db=Depends(get_db)):
    updates = payload.model_dump(exclude_none=True)
    return await orders_repo.update_order(db, order_id, updates)

@app.delete("/orders/{order_id}")
async def delete_order_endpoint(order_id: str, db=Depends(get_db)):
    await orders_repo.delete_order(db, order_id)
    return {"status": "deleted"}
