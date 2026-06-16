import os
from pony.orm import *
from fastapi.testclient import TestClient
import pytest
import sys
sys.path.append('../src')
from endpoints import app
from crud_handlers import confirm_user, get_match_id, change_in_progress,change_has_ended
from helper_functions import get_websocket_address 
from models import *
client = TestClient(app)

@pytest.fixture(autouse=True)

def setup():

    # Set-up creador de la partida
    data123 = {"username": "usuario124356",
             "password": "HOaaala12345",
             "email": "usuario124356@gmail.com"
    }
    client.post("/register/", data123)
    confirm_user("usuario124356")

    response = client.post("/login/", 
            data = {"username": 'usuario124356', "password": 'HOaaala12345'})

    token1 = response.json()['access_token']

    f = open("test.py", "w")

    client.post("/robot/", data = {"robotName": "Robot1"},
        files={"robotCode": ("test.py", open("test.py", "rb"))},
    headers = {"Authorization": f"Bearer {token1}"})
    f.close()

    # Se crea la partida 1 (sin contraseña)
    data = { "nombre_partida" : 'aaepartidaa', 
            "cant_rondas" : 250, 
            "cant_juegos" : 20, 
            "cant_max_players" : 2,
        }

    client.post("/crear_partida/", 
            data = data, headers = {"Authorization": f"Bearer {token1}"})

    # Se crea la partida 2 (Con contraseña)
    data = { "nombre_partida" : 'partiduli12', 
            "cant_rondas" : 520, 
            "cant_juegos" : 20, 
            "cant_max_players" : 3,
            "password":'HOaaala12345'
        }
    client.post("/crear_partida/", 
            data = data, headers = {"Authorization": f"Bearer {token1}"})



def test_partida_en_progreso():
    # Set-Up jugador 2
    data2 = {"username": "jugadorpepe",
             "password": "HOaaala12345",
             "email": "jugadorpartida123_pyrobots@gmail.com"
    }
    client.post("/register/", data2)
    confirm_user("jugadorpepe")
    response = client.post("/login/", 
            data = {"username": 'jugadorpepe', "password": 'HOaaala12345'})

    token2 = response.json()['access_token']

    f = open("test2.py", "w")
    client.post("/robot/", data = {"robotName": "Robot2"},
        files={"robotCode": ("test2.py", open("test2.py", "rb"))},
        headers = {"Authorization": f"Bearer {token2}"})

    f.close()

    # Lo seteo a en progreso para el caso de test
    change_in_progress("aaepartidaa", True)
    response = client.post("/partida/unirse/", data = {"match_name" : "aaepartidaa", "robot_name" : "Robot2"},
    headers = {"Authorization": f"Bearer {token2}"})


    assert response.status_code == 409
    assert response.json() == {
        "detail" : "La partida esta en proceso o ya ha terminado"}
    change_in_progress("aaepartidaa", False)

    
def test_partida_finalizada():
    # cambiar a finalizda
    change_has_ended("aaepartidaa", True)

    response = client.post("/login/", 
    data = {"username": 'jugadorpepe', "password": 'HOaaala12345'})
    token2 = response.json()['access_token']
    response = client.post("/partida/unirse/", data = {"match_name" : "aaepartidaa", "robot_name" : "Robot2"},
            headers = {"Authorization": f"Bearer {token2}"})
    
    assert response.status_code == 409
    assert response.json() == {
        "detail" : "La partida esta en proceso o ya ha terminado"}

    change_has_ended("aaepartidaa", False)

def test_partida_no_existe():
    response = client.post("/login/", 
    data = {"username": 'jugadorpepe', "password": 'HOaaala12345'})
    token2 = response.json()['access_token']
    response = client.post("/partida/unirse/", data = {"match_name" : "noexistoaaaaa", "robot_name" : "Robot2"},
            headers = {"Authorization": f"Bearer {token2}"})
    
    assert response.status_code == 409
    assert response.json() == {
        "detail" : "El robot o la partida no existen"}


def test_robot_no_existe():
    response = client.post("/login/", 
    data = {"username": 'jugadorpepe', "password": 'HOaaala12345'})
    token2 = response.json()['access_token']
    response = client.post("/partida/unirse/", data = {"match_name" : "aaepartidaa", "robot_name" : "no_existe"},
            headers = {"Authorization": f"Bearer {token2}"})
    
    assert response.status_code == 409
    assert response.json() == {
        "detail" : "El robot o la partida no existen"}


def test_everything_correct_nopassword():
    response = client.post("/login/", 
    data = {"username": 'jugadorpepe', "password": 'HOaaala12345'})
    token2 = response.json()['access_token']
    response = client.post("/partida/unirse/", data = {"match_name" : "aaepartidaa", "robot_name" : "Robot2"},
            headers = {"Authorization": f"Bearer {token2}"})

    lobby = get_match_id('aaepartidaa')
    ws = get_websocket_address(lobby)
    assert response.status_code == 200
    assert response.json() == {
        "detail" : "Usuario unido a partida",
        "websocket" : ws}

def test_wrong_password():
    response = client.post("/login/", 
    data = {"username": 'jugadorpepe', "password": 'HOaaala12345'})
    token2 = response.json()['access_token']
    response = client.post("/partida/unirse/", data = {"match_name" : "partiduli12", "robot_name" : "Robot2", "password" : "estoymal" },
            headers = {"Authorization": f"Bearer {token2}"})

    lobby = get_match_id('partiduli12')
    ws = get_websocket_address(lobby)
    assert response.status_code == 403
    assert response.json() == {
        "detail" : "Contraseña incorrecta"}


def test_no_password():
    response = client.post("/login/", 
    data = {"username": 'jugadorpepe', "password": 'HOaaala12345'})
    token2 = response.json()['access_token']
    response = client.post("/partida/unirse/", data = {"match_name" : "partiduli12", "robot_name" : "Robot2"},
            headers = {"Authorization": f"Bearer {token2}"})

    lobby = get_match_id('partiduli12')
    ws = get_websocket_address(lobby)
    assert response.status_code == 403
    assert response.json() == {
        "detail" : "Contraseña incorrecta"}

def test_everything_correct_password():
    response = client.post("/login/", 
    data = {"username": 'jugadorpepe', "password": 'HOaaala12345'})
    token2 = response.json()['access_token']
    response = client.post("/partida/unirse/", data = {"match_name" : "partiduli12", "robot_name" : "Robot2", "password" : 'HOaaala12345' },
            headers = {"Authorization": f"Bearer {token2}"})

    lobby = get_match_id('partiduli12')
    ws = get_websocket_address(lobby)
    assert response.status_code == 200
    assert response.json() == {
        "detail" : "Usuario unido a partida",
            "websocket" : ws}


def test_player_already_participating():
    response = client.post("/login/", 
    data = {"username": 'jugadorpepe', "password": 'HOaaala12345'})
    token2 = response.json()['access_token']
    response = client.post("/partida/unirse/", data = {"match_name" : "aaepartidaa", "robot_name" : "Robot2"},
            headers = {"Authorization": f"Bearer {token2}"})
    assert response.status_code == 403
    assert response.json() == {
        "detail" : "Ya esta unido a la partida"}


def test_maximo_jugadores_alcanzado():

    # Set-up jugador 3
    data = {"username": "jugadorno",
             "password": "HOaaala12345",
             "email": "pyrobotsnoentro@gmail.com"
    }
    client.post("/register/", data)
    confirm_user("jugadorno")
    response = client.post("/login/", 
            data = {"username": 'jugadorno', "password": 'HOaaala12345'})
    token = response.json()['access_token']

    f = open("test3.py", "w")
    client.post("/robot/", data = {"robotName": "Robot3"},
        files={"robotCode": ("test3.py", open("test3.py", "rb"))},
        headers = {"Authorization": f"Bearer {token}"})

    f.close()
    response = client.post("/partida/unirse/", data = {"match_name" : "aaepartidaa", "robot_name" : "Robot3"},
            headers = {"Authorization": f"Bearer {token}"})
    
    assert response.status_code == 403
    assert response.json() == {
        "detail" : "La partida esta llena"}

    os.remove("test.py")
    os.remove("test2.py")
    os.remove("test3.py")
