def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Flask ChatBot" in response.data


def test_get_bot_response(client):
    response = client.get("/get", query_string={"msg": "hello"})
    assert response.status_code == 200
    assert response.data == b"echo: hello"


def test_get_bot_response_escapes_user_input_client_side(client):
    # The server just echoes whatever the fake bot returns; XSS protection
    # for rendered chat bubbles lives in app/static/chat.js (escapeHtml),
    # not on the server, since /get returns plain text, not HTML.
    response = client.get("/get", query_string={"msg": "<script>alert(1)</script>"})
    assert response.status_code == 200
    assert response.data == b"echo: <script>alert(1)</script>"


def test_get_bot_response_missing_msg(client):
    response = client.get("/get")
    assert response.status_code == 200
    assert response.data == b"echo: "
