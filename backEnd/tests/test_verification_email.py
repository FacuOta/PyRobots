from pony.orm import *
from fastapi.testclient import TestClient
import pytest

import sys
sys.path.append('../src')
from crud_handlers import get_user, confirm_user
from endpoints import app

client = TestClient(app)

def test_unverified_user():
    client.post(
        "/register/", 
        data = {
            "username": "user1278",
            "password": "Password1234",
            "email": "transformers.pyrobots@gmail.com"
        })

    user = get_user("user1278")
    assert(user.is_verified == False)

    response = client.post("/send_verif_email/", data = {"username" : "user1278"})
    assert response.status_code == 200
    assert response.json() == {
        "detail": "Email enviado correctamente"
    }


def test_verified_user():

    #confirmo el usuario
    confirm_user("user1278") 

    #verificacion de que se haya cambiado el Bool correctamente
    user = get_user("user1278")
    assert(user.is_verified == True)

    response = client.post("/send_verif_email/", data = {"username" : "user1278"})

    assert response.status_code == 401
    assert response.json() == {
        "detail":"Usuario ya confirmado"}


def test_non_existent_username():

    response = client.post("/send_verif_email/", data = {"username" : "NOEXISTOAAAAAAAAA"})

    assert response.status_code == 400
    assert response.json() == {
        "detail":"Usuario no existe"}