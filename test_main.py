from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == ("AI CODE REVIEWER is running")

def test_valid_code():
    response = client.post("/analyze", json = {"code":"def add(a, b):\n    return a + b"})
    assert response.status_code == 200
    assert response.json()["valid"] == True

def test_invalid_code():
    response = client.post("/analyze", json = {"code":"def add(a, b)\n    return a + b"})
    assert response.status_code == 200
    assert response.json()["valid"] == False
    assert "error" in response.json()

def test_empty_code_rejected():
    response = client.post("/analyze",json={"code": ""})
    assert response.status_code == 422


def test_code_length_limit():
    response = client.post("/analyze",json={"code": "x" * 10001})
    assert response.status_code == 422
