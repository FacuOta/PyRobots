from pony.orm import *
from fastapi.testclient import TestClient
import pytest
import os
import sys
sys.path.append('../src')
from endpoints import app
from crud_handlers import confirm_user

client = TestClient(app)

@pytest.fixture(autouse = True)
def setUp():
    dataM = {"username": "Marcos",
             "password": "Password1234",
             "email": "Marcos@gmail.com"
    }
    dataJu = {"username" : "Juan",
             "password" : "Password1234",
             "email" : "Juan@gmail.com"
    }
    dataF = {"username": "Fran",
             "password": "Password1234",
             "email": "Fran@gmail.com"
    }
    dataJo = {"username" : "Jose",
             "password" : "Password1234",
             "email" : "Jose@gmail.com"
    }
    client.post("/register/", dataF)
    confirm_user("Fran")
    client.post("/register/", dataJo)
    confirm_user("Jose")
    client.post("/register/", dataM)
    confirm_user("Marcos")
    client.post("/register/", dataJu)
    confirm_user("Juan")

def test_normal_upload_no_avatar():
    data = {"username": 'Fran', "password": 'Password1234'}
    response = client.post("/login/", data = data)

    token = response.json()['access_token']

    f = open("test.py", "w")

    response = client.post(
    "/robot/",
    data = {
        "robotName": "Robot1"
    },
    files={
        "robotCode": ("test.py", open("test.py", "rb"))
    },
    headers = {"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    assert response.json() == {
        "detail": "Robot created"
    }
    f.close()
    os.remove("test.py")

def test_normal_upload_avatar():
    data = {"username": 'Jose', "password": 'Password1234'}

    response = client.post("/login/", data = data)

    token = response.json()['access_token']

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
    assert response.status_code == 201
    assert response.json() == {
        "detail": "Robot created"
    }
    f.close()
    g.close()
    os.remove("test.py")
    os.remove("testAvatar.jpg")

def test_non_unique_robotName():
    data = {"username": 'Fran', "password": 'Password1234'}
    response = client.post("/login/", data = data)

    token = response.json()['access_token']

    f = open("test.py", "w")

    response = client.post(
    "/robot/",
    data = {
        "robotName": "Robot1"
    },
    files={
        "robotCode": ("test.py", open("test.py", "rb"))
    },
    headers = {"Authorization": f"Bearer {token}"})
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Non-unique robot name"
    }
    f.close()
    os.remove("test.py")

def test_long_robotName():
    data = {"username": 'Fran', "password": 'Password1234'}
    response = client.post("/login/", data = data)

    token = response.json()['access_token']

    f = open("test.py", "w")

    response = client.post(
    "/robot/",
    data = {
        "robotName": "Robot1234567890abcd"
    },
    files={
        "robotCode": ("test.py", open("test.py", "rb"))
    },
    headers = {"Authorization": f"Bearer {token}"})
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Invalid robot name"
    }
    f.close()
    os.remove("test.py")

def test_invalid_robot_avatar():
    data = {"username": 'Marcos', "password": 'Password1234'}

    response = client.post("/login/", data = data)

    token = response.json()['access_token']

    f = open("test.py", "w")
    g = open("testAvatar.exe", "w")

    response = client.post(
    "/robot/",
    data = {
        "robotName": "Robot123"
    },
    files={
        "robotCode": ("test.py", open("test.py", "rb")),
        "robotAvatar": ("testAvatar.exe", open("testAvatar.exe", "rb"), "executable")
    },
    headers = {"Authorization": f"Bearer {token}"})
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Invalid image"
    }
    f.close()
    g.close()
    os.remove("test.py")
    os.remove("testAvatar.exe")
