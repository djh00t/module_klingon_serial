import pytest
from starlette.testclient import TestClient
from openfaas.handler import app

client = TestClient(app)

def test_root_default_json():
    response = client.get("/")
    assert response.status_code == 406
    assert response.headers['content-type'] == 'application/json'
    assert 'detail' in response.json()

def test_root_accept_json():
    response = client.get("/", headers={"Accept": "application/json"})
    assert response.status_code == 200
    assert response.headers['content-type'] == 'application/json'
    assert 'serial' in response.json()

def test_root_accept_plain_text():
    response = client.get("/", headers={"Accept": "text/plain"})
    assert response.status_code == 200
    assert response.headers['content-type'] == 'text/plain; charset=utf-8'
    assert len(response.text) > 0

def test_root_accept_html():
    response = client.get("/", headers={"Accept": "text/html"})
    assert response.status_code == 200
    assert response.headers['content-type'] == 'text/html; charset=utf-8'
    assert '<p>' in response.text

def test_root_accept_xml():
    response = client.get("/", headers={"Accept": "application/xml"})
    assert response.status_code == 200
    assert response.headers['content-type'] == 'application/xml'
    assert '<serial>' in response.text

def test_root_accept_xhtml():
    response = client.get("/", headers={"Accept": "application/xhtml+xml"})
    assert response.status_code == 200
    assert response.headers['content-type'] == 'text/html; charset=utf-8'
    assert '<p>' in response.text

def test_root_invalid_accept_header():
    response = client.get("/", headers={"Accept": "application/invalid"})
    assert response.status_code == 406
    assert response.headers['content-type'] == 'application/json'
    assert 'detail' in response.json()
#    assert 'error' in response.json()
def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.text == "OK"
