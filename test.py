from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_login_mauvais_identifiants():
    response = client.post(
        "/login",
        data={"username": "chiama", "password": "123523"}
    )
    assert response.status_code == 401
    
def test_traduire_sans_token():
    response = client.post("/traduire", json={"text": "hello", "sens": "en-fr"})
    assert response.status_code == 401