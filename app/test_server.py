from fastapi.testclient import TestClient

from .server import app

client = TestClient(app)

def test_get_login():
    response = client.get("/login")
    assert response.status_code == 200

def test_post_login():
    response = client.post(
        "/login", 
        headers={"Authorization": "Bearer wrong_token"}, 
        data={"username": "admin", "password": "admin"}
    )
    assert response.status_code == 200
    assert "Authorization" in response.headers

def test_post_signup():
    response = client.post(
        "/signup",
        data={"username": "user1", "password": "user1"}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Sign-up successful, awaiting admin approval"}

def test_get_transcribe():
    response = client.get("/transcribe", headers={"Authorization": "Bearer wrong_token"})
    assert response.status_code == 401

def test_post_transcribe():
    response = client.post("/transcribe", headers={"Authorization": "Bearer wrong_token"})
    assert response.status_code == 401
