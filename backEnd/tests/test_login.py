from pony.orm import *
from fastapi.testclient import TestClient
import pytest

import sys
sys.path.append('../src')
from endpoints import app
from crud_handlers import confirm_user
client = TestClient(app)

@pytest.fixture(autouse = True)
def setUpUsers():
    dataJ = {"username": "Juanjo",
             "password": "JOadnn223",
             "email": "Juanjo@gmail.com"
    }
    dataP = {"username" : "Pedrito",
             "password" : "ksdfSDfn212",
             "email" : "Pedrito.s@gmail.com"
    }
    client.post("/register/", dataJ)
    client.post("/register/", dataP)
    confirm_user("Pedrito")

def test_existing_user():
    data = {"username": 'Pedrito', "password": 'ksdfSDfn212'}
    response = client.post("/login/", data = data)

    assert response.status_code == 200

def test_bad_username():
    data = {"username": 'Matias', "password": 'Tasjn945ls'}
    response = client.post("/login/", data = data)

    assert response.status_code == 401
    assert response.json() == {"detail" : "Incorrect Username or Password"}

def test_incorrect_password():
    data = {"username": 'Juanjo', "password": 'Abcde7545'}
    response = client.post("/login/", data = data)

    assert response.status_code == 401
    assert response.json() == {"detail" : "Incorrect Username or Password"}

def test_unverified_user_login():
    data = {"username": 'Juanjo', "password": 'JOadnn223'}
    response = client.post("/login/", data = data)

    assert response.status_code == 401
    assert response.json() == {"detail" : "User has not verified its email adress"}