import os
import pytest
import requests
from pymongo import MongoClient


@pytest.fixture(autouse=True)
def clean_orders_collection():
    mongo_uri = os.getenv("MONGO_URI", "mongodb://mongo:27017")
    db_name = os.getenv("MONGO_DB", "orders_db")

    # If tests run with pytest-xdist, each worker gets its own DB to avoid collisions
    worker_id = os.getenv("PYTEST_XDIST_WORKER")  # e.g. "gw0", "gw1", ...
    if worker_id:
        db_name = f"{db_name}_{worker_id}"

    client = MongoClient(mongo_uri)
    db = client[db_name]

    db["orders"].delete_many({})

    yield

    db["orders"].delete_many({})
    client.close()


@pytest.fixture
def base_url():
    return os.getenv("BASE_URL", "http://api:8000")


@pytest.fixture
def create_order(base_url):
    def _create(payload):
        resp = requests.post(f"{base_url}/orders", json=payload)
        data = resp.json()
        return data
    return _create


@pytest.fixture
def order_payload():
    return {
        "user_id": "u_test_1",
        "items": [
            {"product_id": "p001", "name": "Laptop", "price": 1200, "quantity": 1},
            {"product_id": "p002", "name": "Mouse", "price": 25, "quantity": 2},
        ],
        "total_price": 1250,
        "status": "Pending",
    }


@pytest.fixture
def created_order(create_order, order_payload):
    return create_order(order_payload)
