import pytest

def test_ping(client):

    payload = {
        "jsonrpc": "2.0",
        "method": "ping",
        "id": 1,
    }

    # response = client.post(path="/rpc/", data=payload, content_type="application/json-rpc", follow=True)
    response = client.get(path="/rpc/", follow=True)
    assert response.status_code == 200
