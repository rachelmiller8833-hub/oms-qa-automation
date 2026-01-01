from bson import ObjectId
from fastapi import HTTPException


def _to_object_id(order_id: str) -> ObjectId:
    # Convert string ID to MongoDB ObjectId and fail fast if invalid
    try:
        return ObjectId(order_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Order not found")


async def insert_order(db_handle, order_dict: dict) -> str:
    # Insert a new order document and return its generated ID
    res = await db_handle["orders"].insert_one(order_dict)
    return str(res.inserted_id)


async def find_order(db_handle, order_id: str) -> dict:
    # Retrieve a single order by ID
    oid = _to_object_id(order_id)
    doc = await db_handle["orders"].find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="Order not found")

    # Convert ObjectId to string for API response
    doc["_id"] = str(doc["_id"])
    return doc


async def update_order(db_handle, order_id: str, updates: dict) -> dict:
    # Update only provided fields for an existing order
    oid = _to_object_id(order_id)

    if not updates:
        raise HTTPException(status_code=400, detail="No fields provided for update")

    res = await db_handle["orders"].update_one({"_id": oid}, {"$set": updates})
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Order not found")

    doc = await db_handle["orders"].find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="Order not found")

    doc["_id"] = str(doc["_id"])
    return doc


async def delete_order(db_handle, order_id: str) -> None:
    # Delete an order by ID
    oid = _to_object_id(order_id)

    res = await db_handle["orders"].delete_one({"_id": oid})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Order not found")
