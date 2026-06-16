from pony.orm import *
from fastapi.testclient import TestClient
import pytest
import sys
sys.path.append('../src')
from endpoints import app
from crud_handlers import confirm_user, get_match_id

client = TestClient(app)

@pytest.fixture(autouse=True)
def setUpUsers():
    data123 = {"username": "usuario123456",
             "password": "HOaaala12345",
             "email": "usuario123456@gmail.com"
    }
    client.post("/register/", data123)
    confirm_user("usuario123456")

def test_partida_correcta():

    data = {"username": 'usuario123456', "password": 'HOaaala12345'}
    response = client.post("/login/", data = data)
    token = response.json()['access_token']
    
    data = { "nombre_partida" : 'nombre_partida', 
            "cant_rondas" : 200, 
            "cant_juegos" : 20, 
            "cant_max_players" : 4,
            "password":'HOaaala12345'
        }
    response = client.post("/crear_partida/", 
        data = data, headers = {"Authorization": f"Bearer {token}"})

    assert response.status_code == 201

    lobby_id = get_match_id("nombre_partida")
    
    assert response.json() == {
        "detail": "Partida Creada",
        "websocket" : "ws://localhost:8000/lobbys/" + str(lobby_id)
    }

def test_partida_correcta_SinPassword():

    data = {"username": 'usuario123456', "password": 'HOaaala12345'}
    response = client.post("/login/", data = data)
    token = response.json()['access_token']
    data = { "nombre_partida" : 'nombre_partida1', 
            "Creador" : 'usuario123456',  
            "cant_rondas" : 250, 
            "cant_juegos" : 20, 
            "cant_max_players" : 4,
        }
    response = client.post("/crear_partida/",
    data = data, headers = {"Authorization": f"Bearer {token}"})

    lobby_id = get_match_id('nombre_partida1')

    assert response.status_code == 201
    assert response.json() == {
        "detail": "Partida Creada",
        "websocket" : "ws://localhost:8000/lobbys/" + str(lobby_id)
    }


def test_cant_juegos_invalido():

    data = {"username": 'usuario123456', "password": 'HOaaala12345'}
    response = client.post("/login/", data = data)
    token = response.json()['access_token']
    
    data = { "nombre_partida" : 'nombre_partida', 
            "cant_rondas" : 20, 
            "cant_juegos" : 300000, 
            "cant_max_players" : 4,
            "password":'Hola123456'
        }
    response = client.post("/crear_partida/", 
        data = data, headers = {"Authorization": f"Bearer {token}"})

    assert response.status_code == 401
    assert response.json() == {
        "detail": "cant_juegos_NotValid"
    }


def test_cant_rondas_invalidas():

    data = {"username": 'usuario123456', "password": 'HOaaala12345'}
    response = client.post("/login/", data = data)
    token = response.json()['access_token']
    
    data = { "nombre_partida" : 'nombre_partida', 
            "cant_rondas" : 30000, 
            "cant_juegos" : 20, 
            "cant_max_players" : 4,
            "password":'Hola123456'
        }
    response = client.post("/crear_partida/", 
        data = data, headers = {"Authorization": f"Bearer {token}"})

    assert response.status_code == 401
    assert response.json() == {
        "detail": "cant_rondas_NotValid"
    }

def test_cant_max_players_invalido():

    data = {"username": 'usuario123456', "password": 'HOaaala12345'}
    response = client.post("/login/", data = data)
    token = response.json()['access_token']
    
    data = { "nombre_partida" : 'nombre_partida', 
            "cant_rondas" : 250, 
            "cant_juegos" : 20, 
            "cant_max_players" : 7,
            "password":'Hola123456'
        }
    response = client.post("/crear_partida/", 
        data = data, headers = {"Authorization": f"Bearer {token}"})

    assert response.status_code == 401
    assert response.json() == {
        "detail": "cant_max_player_NotValid"
    }


def test_password_no_valida():
    data = {"username": 'usuario123456', "password": 'HOaaala12345'}
    response = client.post("/login/", data = data)
    token = response.json()['access_token']
    
    data = { "nombre_partida" : 'nombre_partida2', 
            "cant_rondas" : 250, 
            "cant_juegos" : 20, 
            "cant_max_players" : 4,
            "password":'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
        }
    response = client.post("/crear_partida/", 
        data = data, headers = {"Authorization": f"Bearer {token}"})

    assert response.status_code == 401
    assert response.json() == {
        "detail": "PasswordNotValid"
    }


def test_nombre_partida_repetido():
    data = {"username": 'usuario123456', "password": 'HOaaala12345'}
    response = client.post("/login/", data = data)
    token = response.json()['access_token']
    data = { "nombre_partida" : 'nombre_partida', 
            "Creador" : 'usuario123456',  
            "cant_rondas" : 250, 
            "cant_juegos" : 20, 
            "cant_max_players" : 4,
        }
    response = client.post("/crear_partida/",
    data = data, headers = {"Authorization": f"Bearer {token}"})

    
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Nombre de partida no valido"
    }
