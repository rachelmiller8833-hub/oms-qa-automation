import requests


def test_create_order(created_order):
    assert "_id" in created_order and created_order["_id"]


def test_get_order(base_url, created_order, order_payload):
    order_id = created_order["_id"]

    # GET
    get_resp = requests.get(f"{base_url}/orders/{order_id}")
    assert get_resp.status_code == 200, get_resp.text

    fetched = get_resp.json()
    assert fetched["_id"] == order_id
    assert fetched["user_id"] == order_payload["user_id"]
    assert fetched["status"] == order_payload["status"]
    assert fetched["items"] == order_payload["items"]

def test_update_order_put(base_url, created_order, order_payload):
    order_id = created_order["_id"]
    
    before_resp = requests.get(f"{base_url}/orders/{order_id}")
    assert before_resp.status_code == 200, before_resp.text
    before = before_resp.json()
    original_items = before["items"]

    update_payload = {"status": "Shipped"}

    update_resp = requests.put(f"{base_url}/orders/{order_id}", json=update_payload)
    assert update_resp.status_code == 200, update_resp.text

    updated = update_resp.json()
    assert updated["_id"] == order_id
    assert updated["user_id"] == order_payload["user_id"]
    assert updated["status"] == "Shipped"
    # validate PUT doesn't change the items
    assert updated["items"] == original_items

def test_delete_order(base_url, created_order):
    order_id = created_order["_id"]

    delete_resp = requests.delete(f"{base_url}/orders/{order_id}")
    assert delete_resp.status_code == 200, delete_resp.text

    delete_body = delete_resp.json()
    assert delete_body["status"] == "deleted"

    # after deleting the order, make sure it doesn't exist anymore
    get_resp = requests.get(f"{base_url}/orders/{order_id}")
    assert get_resp.status_code == 404, get_resp.text

def test_update_nonexistent_order_returns_404(base_url):
    nonexistent_id = "aaaaaaaaaaaaaaaaaaaaaaaa"  # 24-hex string, valid format
    update_payload = {"status": "Shipped"}

    resp = requests.put(f"{base_url}/orders/{nonexistent_id}", json=update_payload)

    assert resp.status_code == 404, resp.text






