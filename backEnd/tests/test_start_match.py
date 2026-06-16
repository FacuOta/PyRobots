from fastapi.testclient import TestClient
import os
import sys
sys.path.append('../src')
from endpoints import app
from crud_handlers import confirm_user, add_robot, get_match_id
from helper_functions import get_websocket_address 
import unittest
import pytest
client = TestClient(app)

@pytest.fixture
def setUp():
    tokenMartin = setUpUsers('Martin', 'Password1234', 'Martin@gmail.com')

    tokenPablo = setUpUsers('Pablo', 'Password1234', 'Pablo@gmail.com')

    add_robot('Martin', 'RobotMartin')
    add_robot('Pablo', 'RobotPablo')
    robot1_code = """class RobotMartin(Robot):
    def initialize(self):
        pass
    def respond(self):
        pass"""
    robot2_code = """import random 
class RobotPablo(Robot):
    def initialize(self):
        self.d = 0
        self.s = -1
    def respond(self):
        self.point_scanner(self.d, 1)
        if self.s != -1:
            self.cannon(self.d, self.s)
        else:
            self.d += 1
            self.s = self.scanned()"""
    file_string1 = "test_files/Martin_RobotMartin.py"
    file_string2 = "test_files/Pablo_RobotPablo.py"
    f = open(file_string1, "w")
    f.write(robot1_code)
    f.close()
    g = open(file_string2, "w")
    g.write(robot2_code)
    g.close()

    return tokenMartin, tokenPablo

@pytest.fixture(scope="function", autouse=True)
def tearDown(request):
    request.addfinalizer(remove_files)

def remove_files():
    os.remove("test_files/Pablo_RobotPablo.py")
    os.remove("test_files/Martin_RobotMartin.py")

def setUpUsers(username, password, email):
    data = {"username": username,
             "password": password,
             "email": email}
    
    client.post("/register/", data)
    confirm_user(username)

    dataVerif = {"username": username, "password": password}
    response = client.post("/login/", data = dataVerif)
    token = response.json()['access_token']

    return token

def test_match(setUp):
    tokenMartin, tokenPablo = setUp
    data = { "nombre_partida" : 'PartidaMartin', 
            "cant_rondas" : 500, 
            "cant_juegos" : 2, 
            "cant_max_players" : 2,
        }

    response = client.post("/crear_partida/", 
            data = data, headers = {"Authorization": f"Bearer {tokenMartin}"})
    
    assert response.status_code == 201
    
    
    response = client.post("/partida/unirse/", data = {"match_name" : "PartidaMartin", "robot_name" : "RobotPablo"},
            headers = {"Authorization": f"Bearer {tokenPablo}"})
    assert response.status_code == 200
    
    lobby = get_match_id('PartidaMartin')
    ws = get_websocket_address(lobby)
    
    response = client.put("/partida/iniciar_partida", data = {"match_name": 'PartidaMartin', 'creator_robot': 'RobotMartin'},
    headers = {"Authorization": f"Bearer {tokenMartin}"})

    id = get_match_id('PartidaMartin')
    match = client.get(f"/partida/{id}/resultados", headers = {"Authorization": f"Bearer {tokenMartin}"})
    if response.json()['robotGanador'] != '':
        assert match.json()['winnerRobot'] == 'RobotPablo' or match.json()['winnerRobot'] == 'RobotMartin'
    else:
        assert match.json()['winnerRobot'] == ''

    assert response.status_code == 200

def test_usuario_no_creador(setUp):
    tokenMartin, tokenPablo = setUp
    data = { "nombre_partida" : 'PartidaTest', 
            "cant_rondas" : 1000, 
            "cant_juegos" : 40, 
            "cant_max_players" : 2,
        }

    client.post("/crear_partida/", 
            data = data, headers = {"Authorization": f"Bearer {tokenMartin}"})
    client.post("/partida/unirse/", data = {"match_name" : "PartidaMartin", "robot_name" : "RobotPablo"},
            headers = {"Authorization": f"Bearer {tokenPablo}"})
    
    response = client.put("/partida/iniciar_partida", data = {"match_name": 'PartidaTest', 'creator_robot': 'RobotMartin'},
    headers = {"Authorization": f"Bearer {tokenPablo}"})
    
    assert response.status_code == 422
    assert response.json() == {'detail': "El usuario no es el creador"}

def test_no_suficientes_jugadores(setUp):
    tokenMartin, tokenPablo = setUp
    data = { "nombre_partida" : 'PartidaEjemplo', 
            "cant_rondas" : 1000, 
            "cant_juegos" : 40, 
            "cant_max_players" : 2,
        }
    
    client.post("/crear_partida/", 
        data = data, headers = {"Authorization": f"Bearer {tokenMartin}"})
    response = client.put("/partida/iniciar_partida", data = {"match_name": 'PartidaEjemplo', 'creator_robot': 'RobotMartin'},
    headers = {"Authorization": f"Bearer {tokenMartin}"})

    assert response.status_code == 422
    assert response.json() == {'detail': "No hay suficientes jugadores para iniciar"}

def  test_robot_inexistente(setUp):
    tokenMartin, tokenPablo = setUp
    data = { "nombre_partida" : 'PartidaSimulacro', 
            "cant_rondas" : 5000, 
            "cant_juegos" : 96, 
            "cant_max_players" : 3,
        }
    
    client.post("/crear_partida/", 
            data = data, headers = {"Authorization": f"Bearer {tokenMartin}"})
    client.post("/partida/unirse/", data = {"match_name" : "PartidaSimulacro", "robot_name" : "RobotPablo"},
            headers = {"Authorization": f"Bearer {tokenPablo}"})

    id = get_match_id('PartidaSimulacro')

    response = client.put("/partida/iniciar_partida", data = {"match_name": 'PartidaSimulacro', 'creator_robot': 'RobotPablo'},
    headers = {"Authorization": f"Bearer {tokenMartin}"})

    assert response.status_code == 422
    assert response.json() == {'detail': "El usuario no posee el robot ingresado"}

def test_partida_inexistente(setUp):
    tokenMartin, tokenPablo = setUp
    response = client.get("/partida/100/resultados", headers = {"Authorization": f"Bearer {tokenMartin}"})
    assert response.json() == {'detail': 'Partida no existe'}

def test_partida_sin_iniciar(setUp):
    tokenMartin, tokenPablo = setUp
    data = { "nombre_partida" : 'PartidaPrueba', 
            "cant_rondas" : 1000, 
            "cant_juegos" : 40, 
            "cant_max_players" : 2,
        }

    client.post("/crear_partida/", 
            data = data, headers = {"Authorization": f"Bearer {tokenMartin}"})
    
    id = get_match_id('PartidaPrueba')

    response = client.get(f"/partida/{id}/resultados", headers = {"Authorization": f"Bearer {tokenMartin}"})
    assert response.json() == {'detail': 'Partida en progreso o sin iniciar'}