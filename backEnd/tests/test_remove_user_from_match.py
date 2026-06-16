import os
from pony.orm import *
from fastapi.testclient import TestClient
import pytest
import sys
sys.path.append('../src')
from endpoints import app
from crud_handlers import confirm_user, change_in_progress,change_has_ended, get_robot, get_user, get_Partida
from models import *
client = TestClient(app)

@pytest.fixture(autouse=True)

def setup():

    # Set-up de un jugador
    data = {"username": "usuar1356",
             "password": "HOaaala12345",
             "email": "usuar1356@gmail.com"
    }
    client.post("/register/", data)
    confirm_user("usuar1356")

    f = open("test.py", "w")

    response = client.post("/login/", 
    data = {"username": 'usuar1356', "password": 'HOaaala12345'})

    token2 = response.json()['access_token']


    client.post("/robot/", data = {"robotName": "Robot5"},
        files={"robotCode": ("test.py", open("test.py", "rb"))},
    headers = {"Authorization": f"Bearer {token2}"})
    f.close()    

    # Set-up creador de la partida
    data123 = {"username": "usuario1356",
             "password": "HOaaala12345",
             "email": "usuario1356@gmail.com"
    }
    client.post("/register/", data123)
    confirm_user("usuario1356")

    response = client.post("/login/", 
            data = {"username": 'usuario1356', "password": 'HOaaala12345'})

    token1 = response.json()['access_token']

    f = open("test.py", "w")

    client.post("/robot/", data = {"robotName": "Robot1"},
        files={"robotCode": ("test.py", open("test.py", "rb"))},
    headers = {"Authorization": f"Bearer {token1}"})
    f.close()


    # Set up partida

    data = { "nombre_partida" : "partidaoriginal", 
            "cant_rondas" : 250, 
            "cant_juegos" : 20, 
            "cant_max_players" : 4,
        }
    response = client.post("/crear_partida/", 
    data = data, headers = {"Authorization": f"Bearer {token1}"})

def test_userNotParticipating():

    response = client.post("/login/", 
            data = {"username": 'usuar1356', "password": 'HOaaala12345'})

    token = response.json()['access_token']

    response = client.put("/partida/abandonar/", 
            data = {"match_name" : "partidaoriginal" }, headers = {"Authorization": f"Bearer {token}"})
    
    assert response.status_code == 409
    assert response.json() == {"detail" : "User is not a player in that match"}


def test_NonExistentMatch():

    response = client.post("/login/", 
            data = {"username": 'usuar1356', "password": 'HOaaala12345'})

    token = response.json()['access_token']

    response = client.put("/partida/abandonar/", 
            data = {"match_name" : "noexistoaaaaedsasaadskjf" }, headers = {"Authorization": f"Bearer {token}"})
    
    assert response.status_code == 409
    assert response.json() == {"detail" : "Match does not exist"}


def test_remove_creator():

    response = client.post("/login/", 
            data = {"username": 'usuario1356', "password": 'HOaaala12345'})

    token = response.json()['access_token']

    response = client.put("/partida/abandonar/", 
        data = {"match_name" : "partidaoriginal" }, headers = {"Authorization": f"Bearer {token}"})
    
    assert response.status_code == 403
    assert response.json() == {"detail" : "Creator is not allowed to leave its own match"}

@db_session
def test_leave_working():

    response = client.post("/login/", 
            data = {"username": 'usuar1356', "password": 'HOaaala12345'})

    token = response.json()['access_token']

    response = client.post("/partida/unirse/", data = {"match_name" : "partidaoriginal", "robot_name" : "Robot5"},
    headers = {"Authorization": f"Bearer {token}"})

    response = client.put("/partida/abandonar/", 
        data = {"match_name" : "partidaoriginal" }, headers = {"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json() == {"detail" : "Left the match successfully"}

    # Verificación de que robot y el robot ya no esten
    robot = get_robot("usuar1356", "Robot5")
    user = get_user("usuar1356")
    p = get_Partida("partidaoriginal")
    assert(robot not in p.robots)
    assert(user not in p.Participan)



def test_game_over():
    response = client.post("/login/", 
        data = {"username": 'usuar1356', "password": 'HOaaala12345'})

    token = response.json()['access_token']

    change_has_ended("partidaoriginal", True)
    response = client.put("/partida/abandonar/", 
        data = {"match_name" : "partidaoriginal" }, headers = {"Authorization": f"Bearer {token}"})


    change_has_ended("partidaoriginal", False)
    assert response.status_code == 409
    assert response.json() == {"detail" : "Match is either in progress or has already ended"}

def test_match_in_progress():

    response = client.post("/login/", 
        data = {"username": 'usuar1356', "password": 'HOaaala12345'})

    token = response.json()['access_token']

    change_in_progress("partidaoriginal", True)
    response = client.put("/partida/abandonar/", 
        data = {"match_name" : "partidaoriginal" }, headers = {"Authorization": f"Bearer {token}"})

    change_in_progress("partidaoriginal", False)
    assert response.status_code == 409
    assert response.json() == {"detail" : "Match is either in progress or has already ended"}
    
    os.remove("test.py")
