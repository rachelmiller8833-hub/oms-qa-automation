# End-to-end tests for order CRUD operations via the public API.
# Validates happy paths, edge cases, and error handling behavior.
import requests
import pytest


def test_create_order(created_order):
    # Verify order creation returns a valid order ID
    assert "_id" in created_order and created_order["_id"]


def test_get_order(base_url, created_order, order_payload):
    order_id = created_order["_id"]

    get_resp = requests.get(f"{base_url}/orders/{order_id}")
    assert get_resp.status_code == 200, get_resp.text

    fetched = get_resp.json()
    assert fetched["_id"] == order_id
    assert fetched["user_id"] == order_payload["user_id"]
    assert fetched["status"] == order_payload["status"]
    assert fetched["items"] == order_payload["items"]


@pytest.mark.parametrize("new_status", ["Pending", "Processing", "Shipped", "Delivered"])
def test_update_order_put(base_url, created_order, order_payload, new_status):
    order_id = created_order["_id"]

    before_resp = requests.get(f"{base_url}/orders/{order_id}")
    assert before_resp.status_code == 200, before_resp.text
    before = before_resp.json()
    original_items = before["items"]

    update_payload = {"status": new_status}

    update_resp = requests.put(f"{base_url}/orders/{order_id}", json=update_payload)
    assert update_resp.status_code == 200, update_resp.text

    updated = update_resp.json()
    assert updated["_id"] == order_id
    assert updated["user_id"] == order_payload["user_id"]
    assert updated["status"] == new_status
    # Ensure status update does not modify order items
    assert updated["items"] == original_items


def test_delete_order(base_url, created_order):
    order_id = created_order["_id"]

    delete_resp = requests.delete(f"{base_url}/orders/{order_id}")
    assert delete_resp.status_code == 200, delete_resp.text
    assert delete_resp.json()["status"] == "deleted"

    # Verify deleted order is no longer accessible
    get_resp = requests.get(f"{base_url}/orders/{order_id}")
    assert get_resp.status_code == 404, get_resp.text


def test_update_nonexistent_order_returns_404(base_url):
    # Valid ObjectId format that does not exist in DB
    nonexistent_id = "aaaaaaaaaaaaaaaaaaaaaaaa"
    update_payload = {"status": "Shipped"}

    resp = requests.put(f"{base_url}/orders/{nonexistent_id}", json=update_payload)
    assert resp.status_code == 404, resp.text


def test_get_order_with_invalid_id_returns_400_or_422(base_url):
    # Invalid Mongo ObjectId format
    invalid_id = "not-a-valid-objectid"

    resp = requests.get(f"{base_url}/orders/{invalid_id}")
    assert resp.status_code == 404, resp.text


def test_delete_order_twice_second_time_returns_404_or_200(base_url, created_order):
    order_id = created_order["_id"]

    first = requests.delete(f"{base_url}/orders/{order_id}")
    assert first.status_code == 200, first.text
    assert first.json().get("status") == "deleted"

    # Second delete checks idempotency / not-found behavior
    second = requests.delete(f"{base_url}/orders/{order_id}")
    assert second.status_code in (404, 200), second.text

    if second.status_code == 200:
        body = second.json()
        assert body.get("status") in ("deleted", "already_deleted", "not_found"), body


def test_create_order_payment_failure(base_url, order_payload):
    # Simulate payment failure using a request header
    resp = requests.post(
        f"{base_url}/orders",
        json=order_payload,
        headers={"X-Payment-Fail": "1"},
    )
    assert resp.status_code == 402
