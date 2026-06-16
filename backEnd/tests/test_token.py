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
    dataM = {"username": "Marisa",
             "password": "JOadnn223",
             "email": "marisa@gmail.com"
    }
    dataG = {"username" : "Gonzalo",
             "password" : "ksdfSDfn212",
             "email" : "gonza.s@gmail.com"
    }
    client.post("/register/", dataM)
    client.post("/register/", dataG)
    confirm_user("Marisa")
    confirm_user("Gonzalo")

def test_good_token():
    data = {"username": 'Marisa', "password": 'JOadnn223'}
    response = client.post("/login/", data = data)

    token = response.json()['access_token']

    token_key = client.get("/users/me",
                            headers = {"Authorization": f"Bearer {token}"}) 

    assert token_key.status_code == 200
    assert token_key.json() == {"username" : 'Marisa', "email" : 'marisa@gmail.com'}

def test_bad_token():
    data = {"username": 'Marisa', "password": 'JOadnn223'}
    client.post("/login/", data = data)

    token_key = client.get("/users/me",
                            headers = {"Authorization": "Bearer jbadjsbdfjsbjdbjadcnanskdfnajnef"}) 

    assert token_key.status_code == 401
    assert token_key.json() == {'detail' : "Could not validate credentials"}