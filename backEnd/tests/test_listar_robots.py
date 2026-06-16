from pony.orm import *
from fastapi.testclient import TestClient
import os
import sys
sys.path.append('../src')
from endpoints import app
from crud_handlers import confirm_user
client = TestClient(app)


def get_token():
    data = {"username": 'Roberto', "password": 'JOadnn223'}
    response = client.post("/login/", data = data)
    print(response)
    token = response.json()['access_token']

    return token

def test_listar():
    dataJ = {"username": "Roberto",
             "password": "JOadnn223",
             "email": "Roberto@gmail.com"
    }
    client.post("/register/", dataJ)
    confirm_user("Roberto")

    token = get_token()

    f = open("test.py", "w")
    g = open("testAvatar.jpg", "w")

    response = client.post(
    "/robot/",
    data = {
        "robotName": "Robot1"
    },
    files={
        "robotCode": ("test.py", open("test.py", "rb")),
        "robotAvatar": ("testAvatar.jpg", open("testAvatar.jpg", "rb"), "image/jpeg")
    },
    headers = {"Authorization": f"Bearer {token}"})

    f.close()
    g.close()
    os.remove("test.py")
    os.remove("testAvatar.jpg")


    response = client.get("/get_robots/",
                        headers = {"Authorization": f"Bearer {token}"})
    
    assert response.json() == {
        "robotNames": ['Robot1']
    }
