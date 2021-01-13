import json
import pytest


def test_division(client):

    payload = {
        "jsonrpc": "2.0",
        "method": "division",
        "params": {
            "dividend": 1080,
            "divisor": 16,
        },
        "id": 1,
    }

    response = client.post(
        path="/rpc/", data=payload, content_type="application/json-rpc", follow=True,
        HTTP_X_FORWARDED_FOR="192.168.1.2,10.20.30.40,127.0.0.1"
    )
    assert response.status_code == 200

    content = json.loads(response.content)
    assert content["result"]["quotient"] == 67
    assert content["result"]["remainder"] == 8
    assert content["result"]["ipaddress"] == "192.168.1.2"

# HTTP_X_FORWARDED_FOR の値とレスポンスステータス
host_x_headers = (
    ("192.168.1.2,127.0.0.1", 200),
    ("192.168.2.2,127.0.0.1", 400),
    ("192.168.1.254,127.0.0.1", 200),
    ("10.20.30.1,192.168.1.1", 400),
)

@pytest.mark.parametrize("x_header, http_status", host_x_headers)
def test_client_address(client, x_header, http_status):

    payload = {
        "jsonrpc": "2.0",
        "method": "division",
        "params": {"dividend": 1080, "divisor": 16},
        "id": 1,
    }

    response = client.post(
        path="/rpc/", data=payload, content_type="application/json-rpc", follow=True,
        HTTP_X_FORWARDED_FOR=x_header
    )
    assert response.status_code == http_status
