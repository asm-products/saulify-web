from flask import url_for


def test_app(client):
    assert client.get(url_for('index')).status_code == 200
