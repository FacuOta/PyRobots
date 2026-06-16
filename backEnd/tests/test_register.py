from pony.orm import *
import sys
sys.path.append('../src')
from endpoints import app
from fastapi.testclient import TestClient
import os

client = TestClient(app)


def test_long_username():
    response = client.post(
        "/register/", 
        data = {
            "username": "Usuario1234567890",
            "password": "Password1234",
            "email": "TestEmail@gmail.com"
        })
    
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Invalid username"
    }

def test_correct_username():
    response = client.post(
        "/register/", 
        data = {
            "username": "Usuario123456789",
            "password": "Password1234",
            "email": "TestUsername@gmail.com"
        })
    
    assert response.status_code == 201
    assert response.json() == {
        "detail": "User created"
    }
def test_repeat_uesrname():
    response = client.post(
        "/register/", 
        data = {
            "username": "Usuario123456789",
            "password": "Password1234",
            "email": "TestUsername@gmail.com"
        })
    
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Non-unique email or username"
    }

def test_short_password():
    response = client.post(
        "/register/", 
        data = {
            "username": "User",
            "password": "pass",
            "email": "TestEmail@gmail.com"
        })
    
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Invalid password"
    }

def test_long_password():
    response = client.post(
        "/register/", 
        data = {
            "username": "User",
            "password": "Password1234567890",
            "email": "TestEmail@gmail.com"
        })
    
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Invalid password"
    }

def test_lower_password():
    response = client.post(
        "/register/", 
        data = {
            "username": "User",
            "password": "password1234567890",
            "email": "TestEmail@gmail.com"
        })
    
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Invalid password"
    }

def test_upper_password():
    response = client.post(
        "/register/", 
        data = {
            "username": "User",
            "password": "PASSWORD1234567890",
            "email": "TestEmail@gmail.com"
        })
    
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Invalid password"
    }

def test_nodigit_password():
    response = client.post(
        "/register/", 
        data = {
            "username": "User",
            "password": "PASSWORD",
            "email": "TestEmail@gmail.com"
        })
    
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Invalid password"
    }

def test_correct_password():
    response = client.post(
        "/register/", 
        data = {
            "username": "UserA",
            "password": "Password1234",
            "email": "TestEmail@gmail.com"
        })
    
    assert response.status_code == 201
    assert response.json() == {
        "detail": "User created"
    }

def test_email():
    response = client.post(
        "/register/", 
        data = {
            "username": "User",
            "password": "Password1234",
            "email": "TestEmail"
        })
    
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Invalid email"
    }

def test_correct_email():
    response = client.post(
        "/register/", 
        data = {
            "username": "UserC",
            "password": "Password1234",
            "email": "TestC@gmail.com"
        })
    
    assert response.status_code == 201
    assert response.json() == {
        "detail": "User created"
    }
    

def test_valid_avatar():
    
    f = open("test.jpg", "w")

    response = client.post(
        "/register/",
        data = {
            "username": "UserB",
            "password": "Password1234",
            "email": "TestAvatar@gmail.com",
        },
        files={"avatar": ("test.jpg", open("test.jpg", "rb"), "image/jpeg")}
        
    )
    assert response.status_code == 201
    assert response.json() == {
        "detail": "User created"
    }
    f.close()
    os.remove("test.jpg")

def test_invalid_avatar():
    
    f = open("test.exe", "w")

    response = client.post(
        "/register/",
        data = {
            "username": "UserD",
            "password": "Password1234",
            "email": "TestAvatarD@gmail.com",
        },
        files={"avatar": ("avatar", open("test.exe", "rb"), "executable")}
        
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Invalid image"
    }
    f.close()
    os.remove("test.exe")
