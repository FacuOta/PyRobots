from datetime import datetime
from pony.orm import *
from fastapi.testclient import TestClient
import pytest

import sys
sys.path.append('../src')
from endpoints import app
from crud_handlers import get_match_id, get_user, confirm_user, add_robot, get_robot
from models import Partida
from helper_functions import get_websocket_address

client = TestClient(app)
@pytest.fixture(autouse=True)
def setup_partidas():
    data = {"username": "Ernesto",
             "password": "COntra1232",
             "email": "Ernesto@gmail.com"
    }
    response = client.post("/register/", data)
    confirm_user("Ernesto")
    assert response.status_code == 201
    confirm_user("Ernesto")

    add_robot("Ernesto", "Robot_test")

    with db_session:
        Partida(
            Participan = {get_user("Ernesto")},
            Creador = get_user("Ernesto"),
            robots = {get_robot("Ernesto", "Robot_test")},
            nombre_partida = "partidaterminada1",
            cant_rondas = 500,
            cant_juegos = 50,
            cant_max_players = 4,
            date_time = datetime(2022, 10, 17, 11, 00).isoformat(' '),
            has_ended = True
        )
        Partida(
            Participan = {get_user("Ernesto")},
            Creador = get_user("Ernesto"),
            robots = {get_robot("Ernesto", "Robot_test")},
            nombre_partida = "partidaterminada2",
            cant_rondas = 500,
            cant_juegos = 50,
            cant_max_players = 3,
            date_time = datetime(2022, 10, 16, 11, 00).isoformat(' '),
            has_ended = True,
            ganador = get_robot("Ernesto", "Robot_test")
        )
        Partida(
            Participan = {get_user("Ernesto")},
            Creador = get_user("Ernesto"),
            robots = {},
            nombre_partida = "partidanoterminada",
            cant_rondas = 500,
            cant_juegos = 50,
            cant_max_players = 4,
            date_time = datetime(2022, 10, 14, 11, 00).isoformat(' ')
        ) 

def test_list_ended():

    data = {"username": "Ernesto", "password": "COntra1232"}
    response = client.post("/login/", data = data)
    token = response.json()['access_token']


    response = client.get("/partida/list_ended",
                            headers = {"Authorization": f"Bearer {token}"})
    

    id_1 = get_match_id("partidaterminada1")
    id_2 = get_match_id("partidaterminada2")

    assert response.status_code == 200
    assert response.json() == { 
    'partidas' :
        [
            {
                'id_partida' : id_1,
                'nombre_partida' : 'partidaterminada1',
                'participantes' : ["Ernesto"],
                'robots' : ["Robot_test"],
                'jugadores_participando' : 1,
                'numero_maximo_jugadores' : 4,
                'numero_rondas' : 500, 'numero_juegos' : 50,
                'fecha_creacion' : datetime(2022, 10, 17, 11, 00).isoformat(' '),
                'es_privada' : False, 'es_creador': True, 'participa' : True,
                'termino' : True, 'en_progreso' : False,
                'nombre_ganador' : "", 'robot_ganador' : "",
                'websocket' : get_websocket_address(id_1)
            },
            {
                'id_partida' : id_2,
                'nombre_partida' : "partidaterminada2",
                'participantes' : ["Ernesto"],
                'robots' : ["Robot_test"],
                'jugadores_participando' : 1,
                'numero_maximo_jugadores' : 3,
                'numero_rondas' : 500, 'numero_juegos' : 50,
                'fecha_creacion' : datetime(2022, 10, 16, 11, 00).isoformat(' '),
                'es_privada' : False,'es_creador': True, 'participa' : True,
                'termino' : True, 'en_progreso' : False,
                'nombre_ganador' : "Ernesto", 'robot_ganador' : "Robot_test",
                'websocket' : get_websocket_address(id_2)
            }
        ]
    }
