from datetime import datetime
from pony.orm import *
from fastapi.testclient import TestClient
import pytest

import sys
sys.path.append('../src')
from endpoints import app
from crud_handlers import add_robot, get_robot, get_user, get_match_id, confirm_user
from models import Partida
from helper_functions import get_websocket_address
client = TestClient(app)

@pytest.fixture(scope = 'function', autouse= True)
def setUpUsers():
    dataJ = {"username": "Juan",
             "password": "JOadnn223",
             "email": "juan@gmail.com"
    }
    client.post("/register/", dataJ)
    confirm_user("Juan")

    dataP = {"username" : "Pedro",
             "password" : "ksdfSDfn212",
             "email" : "pedro.s@gmail.com"
    }
    client.post("/register/", dataP)
    confirm_user("Pedro")
    add_robot("Pedro", "RobotP")

    dataG = {"username" : "Gabriel",
             "password" : "FLosmf123x",
             "email" : "g.carid@gmail.com"

    }
    client.post("/register/", dataG)
    confirm_user("Gabriel")
    add_robot("Gabriel", "RobotG")

    dataM = {"username" : "Maria",
             "password" : "KMsmim323",
             "email" : "maria.carid@gmail.com"

    }
    client.post("/register/", dataM)
    confirm_user("Maria")
    add_robot("Maria", "RobotM")
    

@pytest.fixture(scope = 'function')
def setUp_1_Partida():
    with db_session:
        Partida(
            Participan = {get_user("Juan"), get_user("Pedro"),
                          get_user("Gabriel"), get_user("Maria")},
            Creador = get_user("Juan"),
            robots = {get_robot("Pedro", "RobotP"), get_robot("Gabriel", "RobotG"),
                      get_robot("Maria", "RobotM")},
            nombre_partida = "Partida 950",
            cant_rondas = 500,
            cant_juegos = 50,
            cant_max_players = 4,
            date_time = datetime(2022, 10, 17, 11, 00).isoformat(' ')
        )

@pytest.fixture(scope = 'function')
def setUp_2_Partidas():
    with db_session:
        Partida(
            Participan = {get_user("Juan"), get_user("Gabriel"), get_user("Maria")},
            Creador = get_user("Juan"),
            robots = {get_robot("Gabriel", "RobotG"), get_robot("Maria", "RobotM")},
            nombre_partida = "Partida 965",
            cant_rondas = 100,
            cant_juegos = 89,
            cant_max_players = 3,
            date_time = datetime(2022, 10, 17, 11, 00).isoformat(' '),
            password = "ksdflNSKD32",
            has_ended = True,
            ganador = get_robot("Maria", "RobotM")
        )

@pytest.fixture(scope = 'function')
def setUp_Partida_en_progreso():
    with db_session:
        Partida(
            Participan = {get_user("Gabriel"), get_user("Pedro")},
            Creador = get_user("Gabriel"),
            robots = {get_robot("Gabriel", "RobotG"), get_robot("Pedro", "RobotP")},
            nombre_partida = "Partida 963",
            cant_rondas = 500,
            cant_juegos = 50,
            cant_max_players = 4,
            en_progreso = True,
            date_time = datetime(2022, 10, 16, 17, 30).isoformat(' ')
        )

def get_token(username):
    passwords = {"Juan" : 'JOadnn223', "Pedro" : 'ksdfSDfn212'}
    data = {"username": username, "password": passwords[username]}
    response = client.post("/login/", data = data)
    token = response.json()['access_token']

    return token

def test_1_match(setUp_1_Partida):
    token = get_token("Juan")

    match = get_match_id("Partida 950")
    
    response = client.get("/partida/" + str(match),
                            headers = {"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json() == { 
                'id_partida' : match,
                'nombre_partida' : "Partida 950",
                'participantes' : ["Gabriel", "Juan", "Maria", "Pedro"],
                'robots' : ["RobotG", "RobotM", "RobotP"],
                'jugadores_participando' : 4,
                'numero_maximo_jugadores' : 4,
                'numero_rondas' : 500, 'numero_juegos' : 50,
                'fecha_creacion' : datetime(2022, 10, 17, 11, 00).isoformat(' '),
                'es_privada' : False, 'es_creador' : True, 'participa': True,
                'termino' : False, 'en_progreso' : False,
                'nombre_ganador': "", 'robot_ganador': "",
                'websocket' : get_websocket_address(match)
            }


def test_2_match(setUp_2_Partidas):
    token = get_token("Juan")

    match = get_match_id("Partida 965")

    response = client.get("/partida/" + str(match),
                            headers = {"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json() == { 
                'id_partida' : match,
                'nombre_partida' : "Partida 965",
                'participantes' : ["Gabriel", "Juan", "Maria"],
                'robots' : ["RobotG", "RobotM"],
                'jugadores_participando' : 3,
                'numero_maximo_jugadores' : 3,
                'numero_rondas' : 100, 'numero_juegos' : 89,
                'fecha_creacion' : datetime(2022, 10, 17, 11, 00).isoformat(' '),
                'es_privada' : True, 'es_creador' : True, 'participa' : True,
                'termino' : True, 'en_progreso' : False,
                'nombre_ganador' : "Maria", 'robot_ganador' : "RobotM",
                'websocket' : get_websocket_address(match)
            }


def test_3_match(setUp_Partida_en_progreso):
    token = get_token("Pedro")

    match = get_match_id("Partida 963")

    response = client.get("/partida/" + str(match),
                            headers = {"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json() == {
                'id_partida' : match,
                'nombre_partida' : "Partida 963",
                'participantes' : ["Gabriel", "Pedro"],
                'robots' : ["RobotG", "RobotP"],
                'jugadores_participando' : 2,
                'numero_maximo_jugadores' : 4,
                'numero_rondas' : 500, 'numero_juegos' : 50,
                'fecha_creacion' : datetime(2022, 10, 16, 17, 30).isoformat(' '),
                'es_privada' : False, 'es_creador' : False, 'participa' : True,
                'termino' : False, 'en_progreso' : True,
                'nombre_ganador' : "", 'robot_ganador' : "",
                'websocket' : get_websocket_address(match)
            }

def test_bad_id(setUp_1_Partida):
    token = get_token("Pedro")
    response = client.get("/partida/10000",
                          headers = {"Authorization": f"Bearer {token}"})
    
    assert response.status_code == 409
    assert response.json() == {'detail' : "Match 10000 doesn't exist"}