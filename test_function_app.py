import json
import pytest
from function_app import contact_api
from azure.functions import HttpRequest

# Helper to create test request
def create_request(body: dict):
    return HttpRequest(
        method='POST',
        url='/api/contact_api',
        body=json.dumps(body).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )

def test_valid_request():
    req = create_request({
        "name": "Akash",
        "email": "a@example.com",
        "message": "Hello!"
    })
    res = contact_api(req)
    assert res.status_code == 200
    body = json.loads(res.get_body())
    assert body["status"] == "success"

def test_missing_fields():
    req = create_request({"name": "Akash"})
    res = contact_api(req)
    assert res.status_code == 400
    body = json.loads(res.get_body())
    assert body["status"] == "error"

def test_invalid_json():
    req = HttpRequest(
        method='POST',
        url='/api/contact_api',
        body=b"{ bad json",
        headers={'Content-Type': 'application/json'}
    )
    res = contact_api(req)
    assert res.status_code == 500
    body = json.loads(res.get_body())
    assert body["status"] == "error"
