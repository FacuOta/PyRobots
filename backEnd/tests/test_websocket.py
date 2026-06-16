from fastapi.testclient import TestClient
import pytest
import sys
sys.path.append('../src')
from endpoints import app
from crud_handlers import confirm_user, add_robot, get_match_id

client = TestClient(app)

@pytest.fixture(autouse=True)
def setUpUsers():
    dataP = {"username": "Pedro",
             "password": "ksdfSDfn212",
             "email": "pedro.s@gmail.com"
    }
    client.post("/register/", dataP)
    confirm_user("Pedro")
    
    dataJ = {"username": "Juan",
             "password": "JOadnn223",
             "email": "juan@gmail.com"
    }
    client.post("/register/", dataJ)
    confirm_user("Juan")

def get_token_from_user(user: str, password: str):
    data = {"username": user, "password": password}
    response = client.post("/login/", data = data)
    token = response.json()['access_token']

    return token

def submit_to_endpoint(token, endpoint, data):
    return client.post(endpoint,
                        data = data, headers = {"Authorization": f"Bearer {token}"})

def test_websocket():
    with client.websocket_connect("/lobbys/2") as websocket:

        websocket.send_text("Hola Mundo")        
        response = websocket.receive_json()

        assert response == {"Your text" : "Hola Mundo"}
    
def test_websocket_broadcast():
    with client.websocket_connect("/lobbys/1") as websocket_1:
        with client.websocket_connect("/lobbys/1") as websocket_2:
            websocket_1.send_text("Soy uno")
            response1 = websocket_1.receive_json()
            response2 = websocket_2.receive_json()

            assert response1 == {"Your text" : "Soy uno"}
            assert response1 == response2

def test_websocket_lobbys():
    with client.websocket_connect("/lobbys/1") as websocket_1:
        with client.websocket_connect("/lobbys/2") as websocket_2:
            
            websocket_1.send_text("Hola Mundo") 
            websocket_2.send_text("Soy segundo")       
            response1 = websocket_1.receive_json()
            response2 = websocket_2.receive_json()

            assert response1 == {"Your text" : "Hola Mundo"}
            assert response2 == {"Your text" : "Soy segundo"}

def test_partida_socket():
    token = get_token_from_user("Pedro", "ksdfSDfn212")
    match = {
        "nombre_partida" : 'websocket_test', 
        "Creador" : 'Pedro',  
        "cant_rondas" : 900, 
        "cant_juegos" : 50, 
        "cant_max_players" : 4
    }
    enpoint_res = submit_to_endpoint(token, "/crear_partida/",match).json()
    ws = enpoint_res["websocket"]

    with client.websocket_connect(ws) as websocket:
        websocket.send_text("Funciono!")
        response = websocket.receive_json()

        assert response == {"Your text" : "Funciono!"}

def test_join_match_websocket():
    token = get_token_from_user("Juan", "JOadnn223")
    
    add_robot("Juan", "Robot1")

    data = {
        "match_name" : "websocket_test",
        "robot_name" : "Robot1"
    }

    lobby = get_match_id("websocket_test")

    with client.websocket_connect("/lobbys/" + str(lobby)) as websocket:
        endpoint_res = submit_to_endpoint(token, "/partida/unirse/", data)
        assert (endpoint_res.status_code == 200)

        response = websocket.receive_json()

        assert response == {
            "event" : "Union",
            "nombre_usuario" : "Juan"
        }

def test_leave_match_websocket():
    token = get_token_from_user("Juan", "JOadnn223")

    data = {
        "match_name" : "websocket_test",
    }

    lobby = get_match_id("websocket_test")

    with client.websocket_connect("lobbys/" + str(lobby)) as websocket:
        endpoint_res = client.put("/partida/abandonar/",
                        data = data, headers = {"Authorization": f"Bearer {token}"})

        assert (endpoint_res.status_code == 200)

        response = websocket.receive_json()

        assert response == {
            "event" : "Abandona",
            "nombre_usuario" : "Juan"
        }