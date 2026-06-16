from datetime import datetime
from pony.orm import *
from fastapi.testclient import TestClient
import pytest

import sys
sys.path.append('../src')
from endpoints import app
from crud_handlers import add_robot, get_match_id, get_robot, get_user, confirm_user
from models import Partida
from helper_functions import get_websocket_address
client = TestClient(app)

@pytest.fixture
def setUpUsers():
    dataJ = {"username": "Juan",
             "password": "JOadnn223",
             "email": "juan@gmail.com"
    }
    dataP = {"username" : "Pedro",
             "password" : "ksdfSDfn212",
             "email" : "pedro.s@gmail.com"
    }
    client.post("/register/", dataJ)
    client.post("/register/", dataP)
    confirm_user("Juan")
    confirm_user("Pedro")

    add_robot("Pedro", "RobotP")

@pytest.fixture(scope = 'function')
def setUp_1_Partida(setUpUsers):
    with db_session:
        Partida(
            Participan = {get_user("Juan"), get_user("Pedro")},
            Creador = get_user("Juan"),
            robots = {get_robot("Pedro", "RobotP")},
            nombre_partida = "Partida 101",
            cant_rondas = 500,
            cant_juegos = 50,
            cant_max_players = 4,
            date_time = datetime(2022, 10, 17, 11, 00).isoformat(' ')
        )

@pytest.fixture(scope = 'function')
def setUp_2_Partidas():
    with db_session:
        Partida(
            Participan = {get_user("Juan")},
            Creador = get_user("Juan"),
            robots = {},
            nombre_partida = "Partida 32",
            cant_rondas = 100,
            cant_juegos = 89,
            cant_max_players = 3,
            date_time = datetime(2022, 10, 17, 11, 00).isoformat(' ')
        )

@pytest.fixture(scope = 'function')
def setUp_Partida_en_progreso(setUpUsers):
    with db_session:
        Partida(
            Participan = {get_user("Juan"), get_user("Pedro")},
            Creador = get_user("Juan"),
            robots = {get_robot("Pedro", "RobotP")},
            nombre_partida = "Partida 1",
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

def test_none_matches(setUpUsers):
    token = get_token("Pedro")
    response = client.get("/partida/list",
                            headers = {"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json() == { 'partidas' : [] }


def test_match_en_progreso_sin_matches(setUp_Partida_en_progreso):
    token = get_token("Juan")
    response = client.get("/partida/list",
                            headers = {"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json() == { 'partidas' : [] }


def test_existing_1_match(setUp_1_Partida):
    token = get_token("Juan")
    response = client.get("/partida/list",
                            headers = {"Authorization": f"Bearer {token}"})

    id = get_match_id("Partida 101")

    assert response.status_code == 200
    assert response.json() == { 
    'partidas' :
        [
            {
                'id_partida' : id,
                'nombre_partida' : "Partida 101",
                'participantes' : ["Juan", "Pedro"],
                'robots' : ["RobotP"],
                'jugadores_participando' : 2,
                'numero_maximo_jugadores' : 4,
                'numero_rondas' : 500, 'numero_juegos' : 50,
                'fecha_creacion' : datetime(2022, 10, 17, 11, 00).isoformat(' '),
                'es_privada' : False, 'es_creador' : True, 'participa': True,
                'termino' : False, 'en_progreso' : False,
                'nombre_ganador': "", 'robot_ganador': "",
                'websocket' : get_websocket_address(id)
            }
        ]
    }


def test_existing_2_match(setUp_2_Partidas):
    token = get_token("Juan")
    response = client.get("/partida/list",
                            headers = {"Authorization": f"Bearer {token}"})

    id_101 = get_match_id("Partida 101")
    id_32 = get_match_id("Partida 32")

    assert response.status_code == 200
    assert response.json() == { 
    'partidas' :
        [
            {
                'id_partida' : id_101,
                'nombre_partida' : "Partida 101",
                'participantes' : ["Juan", "Pedro"],
                'robots' : ["RobotP"],
                'jugadores_participando' : 2,
                'numero_maximo_jugadores' : 4,
                'numero_rondas' : 500, 'numero_juegos' : 50,
                'fecha_creacion' : datetime(2022, 10, 17, 11, 00).isoformat(' '),
                'es_privada' : False, 'es_creador' : True, 'participa': True,
                'termino' : False, 'en_progreso' : False,
                'nombre_ganador': "", 'robot_ganador': "",
                'websocket' : get_websocket_address(id_101)
            },
            {
                'id_partida' : id_32,
                'nombre_partida' : "Partida 32",
                'participantes' : ["Juan"],
                'robots' : [],
                'jugadores_participando' : 1,
                'numero_maximo_jugadores' : 3,
                'numero_rondas' : 100, 'numero_juegos' : 89,
                'fecha_creacion' : datetime(2022, 10, 17, 11, 00).isoformat(' '),
                'es_privada' : False, 'es_creador' : True, 'participa' : True,
                'termino' : False, 'en_progreso' : False,
                'nombre_ganador' : "", 'robot_ganador' : "",
                'websocket' : get_websocket_address(id_32)
            }
        ]
    }


def test_match_en_progreso_con_matches():
    token = get_token("Juan")
    response = client.get("/partida/list",
                            headers = {"Authorization": f"Bearer {token}"})

    id_101 = get_match_id("Partida 101")
    id_32 = get_match_id("Partida 32")

    assert response.status_code == 200
    assert response.json() == { 
    'partidas' :
        [
            {
                'id_partida' : id_101,
                'nombre_partida' : "Partida 101",
                'participantes' : ["Juan", "Pedro"],
                'robots' : ["RobotP"],
                'jugadores_participando' : 2,
                'numero_maximo_jugadores' : 4,
                'numero_rondas' : 500, 'numero_juegos' : 50,
                'fecha_creacion' : datetime(2022, 10, 17, 11, 00).isoformat(' '),
                'es_privada' : False, 'es_creador' : True, 'participa': True,
                'termino' : False, 'en_progreso' : False,
                'nombre_ganador': "", 'robot_ganador': "",
                'websocket' : get_websocket_address(id_101)
            },
            {
                'id_partida' : id_32,
                'nombre_partida' : "Partida 32",
                'participantes' : ["Juan"],
                'robots' : [],
                'jugadores_participando' : 1,
                'numero_maximo_jugadores' : 3,
                'numero_rondas' : 100, 'numero_juegos' : 89,
                'fecha_creacion' : datetime(2022, 10, 17, 11, 00).isoformat(' '),
                'es_privada' : False, 'es_creador' : True, 'participa' : True,
                'termino' : False, 'en_progreso' : False,
                'nombre_ganador' : "", 'robot_ganador' : "",
                'websocket' : get_websocket_address(id_32)
            }
        ]
    }

def test_list_from_non_creator():
    token = get_token("Pedro")
    response = client.get("/partida/list",
                            headers = {"Authorization": f"Bearer {token}"})

    id_101 = get_match_id("Partida 101")
    id_32 = get_match_id("Partida 32")

    assert response.status_code == 200
    assert response.json() == { 
    'partidas' :
        [
            {
                'id_partida' : get_match_id("Partida 101"),
                'nombre_partida' : "Partida 101",
                'participantes' : ["Juan", "Pedro"],
                'robots' : ["RobotP"],
                'jugadores_participando' : 2,
                'numero_maximo_jugadores' : 4,
                'numero_rondas' : 500, 'numero_juegos' : 50,
                'fecha_creacion' : datetime(2022, 10, 17, 11, 00).isoformat(' '),
                'es_privada' : False, 'es_creador' : False, 'participa': True,
                'termino' : False, 'en_progreso' : False,
                'nombre_ganador': "", 'robot_ganador': "",
                'websocket' : get_websocket_address(id_101)
            },
            {
                'id_partida' : get_match_id("Partida 32"),
                'nombre_partida' : "Partida 32",
                'participantes' : ["Juan"],
                'robots' : [],
                'jugadores_participando' : 1,
                'numero_maximo_jugadores' : 3,
                'numero_rondas' : 100, 'numero_juegos' : 89,
                'fecha_creacion' : datetime(2022, 10, 17, 11, 00).isoformat(' '),
                'es_privada' : False, 'es_creador' : False, 'participa' : False,
                'termino' : False, 'en_progreso' : False,
                'nombre_ganador' : "", 'robot_ganador' : "",
                'websocket' : get_websocket_address(id_32)
            }
        ]
    }