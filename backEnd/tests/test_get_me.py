from fastapi.testclient import TestClient
import pytest
import sys
sys.path.append('../src')
from endpoints import app
from crud_handlers import confirm_user

client = TestClient(app)

@pytest.fixture(autouse=True)
def setUpUsers():
    dataC = {"username": "Cristobal",
             "password": "SantaMaria2",
             "email": "cris.c@gmail.com"
    }
    client.post("/register/", dataC)
    confirm_user("Cristobal")

def get_token_from_user(user: str, password: str):
    data = {"username": user, "password": password}
    response = client.post("/login/", data = data)
    token = response.json()['access_token']

    return token


def test_get_valid_user():
    token = get_token_from_user("Cristobal", "SantaMaria2")

    response = client.get("/users/me", headers = {"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json() == {
        'username' : "Cristobal",
        'email' : 'cris.c@gmail.com'
    }

def test_invalid_token():
    response = client.get("/users/me", headers = {"Authorization": "Bearer mkmsfSAEFMsakmf23knfas"})

    assert response.status_code == 401
    assert response.json() == {'detail' : "Could not validate credentials"}