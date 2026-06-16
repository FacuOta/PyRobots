from fastapi.testclient import TestClient
import os
import sys
sys.path.append('../src')
from endpoints import app
from crud_handlers import confirm_user, add_robot
import unittest

client = TestClient(app)

class OneRobot(unittest.TestCase):
    def setUp(robot1_code):
        file_string1 = "test_files/Lucas_Juan.py"
        f = open(file_string1, "w")
        f.write(robot1_code)
        f.close()

    def tearDown():
        os.remove("test_files/Lucas_Juan.py")

class twoRobots(unittest.TestCase):
    def setUp(robot1_code, robot2_code):
        OneRobot.setUp(robot1_code)
        file_string2 = "test_files/Lucas_Pedro.py"
        g = open(file_string2, "w")
        g.write(robot2_code)
        g.close()

    def tearDown():
        OneRobot.tearDown()
        os.remove("test_files/Lucas_Pedro.py")

class threeRobots(unittest.TestCase):
    def setUp(robot1_code, robot2_code, robot3_code):
        twoRobots.setUp(robot1_code, robot2_code)
        file_string3 = "test_files/Lucas_Andrea.py"
        h = open(file_string3, "w")
        h.write(robot3_code)
        h.close()

    def tearDown():
        twoRobots.tearDown()
        os.remove("test_files/Lucas_Andrea.py")
    
def setUpUsers():
    dataLucas = {"username": "Lucas",
             "password": "Libertad12",
             "email": "Mil@gmail.com"}
    
    client.post("/register/", dataLucas)
    confirm_user('Lucas')

def get_token():
    data = {"username": 'Lucas', "password": 'Libertad12'}
    response = client.post("/login/", data = data)
    token = response.json()['access_token']

    return token 
    
def test_basic_match():
    # Robots no hacen nada. Ningun ganador

    robot1_code = """class Juan(Robot):
    def initialize(self):
        pass
    def respond(self):
        pass"""
    robot2_code = """class Pedro(Robot):
    def initialize(self):
        pass
    def respond(self):
        pass"""
    
    twoRobots.setUp(robot1_code, robot2_code)
    
    setUpUsers()
    token = get_token()
    add_robot('Lucas', 'Juan')
    add_robot('Lucas', 'Pedro')

    url = '?cant_rondas=500&robots=Juan&robots=Pedro&robots=""'

    response = client.post("/simulacion" + url, headers = {"Authorization": f"Bearer {token}"})

    twoRobots.tearDown()
    
    simulation_response = response.json()

    assert (response.status_code == 200)

    assert('usuarioGanador' in simulation_response)
    
    assert ('robotGanador' in simulation_response)
    assert (simulation_response['robotGanador'] == '')

    assert ('robots' in simulation_response)
    assert (simulation_response['robots'] == ['Juan-0', 'Pedro-1'])

    assert ('rondas_robots' in simulation_response)
    assert (len(simulation_response['rondas_robots']) == 2)

    info_rondas_Juan = simulation_response['rondas_robots']['Juan-0']
    
    assert (len(info_rondas_Juan) == 500)

    ronda_1_Juan = info_rondas_Juan[0]

    assert ('is_dead' in ronda_1_Juan)
    assert (not ronda_1_Juan['is_dead'])

    assert ('misiles' in ronda_1_Juan)
    assert (ronda_1_Juan['misiles'] == [])

    assert ('datos_robot' in ronda_1_Juan)
    assert (len(ronda_1_Juan['datos_robot']) == 3)

    datos_Juan = ronda_1_Juan['datos_robot']

    assert ('pos_x' in datos_Juan)
    assert ('pos_y' in datos_Juan)
    assert ('damage' in datos_Juan)

def test_same_robot():
    robot1_code = """class Juan(Robot):
    def initialize(self):
        pass
    def respond(self):
        pass"""
    
    OneRobot.setUp(robot1_code)
    
    setUpUsers()
    token = get_token()
    add_robot('Lucas', 'Juan')

    url = '?cant_rondas=500&robots=Juan&robots=Juan&robots=Juan&robots=Juan'

    response = client.post("/simulacion" + url, headers = {"Authorization": f"Bearer {token}"})

    OneRobot.tearDown()
    
    simulation_response = response.json()

    assert (response.status_code == 200)

    assert('usuarioGanador' in simulation_response)
    
    assert ('robotGanador' in simulation_response)
    assert (simulation_response['robotGanador'] == '')

    assert ('robots' in simulation_response)
    assert (simulation_response['robots'] == ['Juan-0', 'Juan-1', 'Juan-2', 'Juan-3'])

    assert ('rondas_robots' in simulation_response)
    assert (len(simulation_response['rondas_robots']) == 4)

    info_rondas_Juan = simulation_response['rondas_robots']['Juan-2']
    
    assert (len(info_rondas_Juan) == 500)

    ronda_1_Juan = info_rondas_Juan[0]

    assert ('is_dead' in ronda_1_Juan)
    assert (not ronda_1_Juan['is_dead'])

    assert ('misiles' in ronda_1_Juan)
    assert (ronda_1_Juan['misiles'] == [])

    assert ('datos_robot' in ronda_1_Juan)
    assert (len(ronda_1_Juan['datos_robot']) == 3)

    datos_Juan = ronda_1_Juan['datos_robot']

    assert ('pos_x' in datos_Juan)
    assert ('pos_y' in datos_Juan)
    assert ('damage' in datos_Juan)

def test_moving_robot():
    # Robot 2 se choca continuamente contra la pared de abajo. Gana Robot 1

    robot1_code = """class Juan(Robot):
    def initialize(self):
        pass
    def respond(self):
        pass
    """
    robot2_code = """class Pedro(Robot):
    def initialize(self):
        pass
    def respond(self):
        self.drive(270, 30)
    """
    robot3_code = """class Andrea(Robot):
    def initialize(self):
        pass
    def respond(self):
        self.drive(180, 30)
    """

    threeRobots.setUp(robot1_code, robot2_code, robot3_code)
    
    setUpUsers()
    token = get_token()
    add_robot('Lucas', 'Juan')
    add_robot('Lucas', 'Pedro')
    add_robot('Lucas', 'Andrea')

    url = '?cant_rondas=250&robots=Juan&robots=Pedro&robots=Andrea'

    response = client.post("/simulacion" + url, headers = {"Authorization": f"Bearer {token}"})

    threeRobots.tearDown()
    
    simulation_response = response.json()

    assert (response.status_code == 200)

    assert('usuarioGanador' in simulation_response)
    
    assert ('robotGanador' in simulation_response)
    assert (simulation_response['robotGanador'] == 'Juan')

    assert ('robots' in simulation_response)
    assert (simulation_response['robots'] == ['Juan-0', 'Pedro-1', 'Andrea-2'])

    assert ('rondas_robots' in simulation_response)
    assert (len(simulation_response['rondas_robots']) == 3)

    info_rondas_Pedro = simulation_response['rondas_robots']['Pedro-1']
    rondas = len(info_rondas_Pedro)

    assert (len(info_rondas_Pedro) <= 250)

    ronda_1_Pedro = info_rondas_Pedro[rondas-1]

    assert ('is_dead' in ronda_1_Pedro)
    assert (ronda_1_Pedro['is_dead'])

    assert ('misiles' in ronda_1_Pedro)
    assert (ronda_1_Pedro['misiles'] == [])

    assert ('datos_robot' in ronda_1_Pedro)
    assert (len(ronda_1_Pedro['datos_robot']) == 3)

    datos_Pedro = ronda_1_Pedro['datos_robot']

    assert ('pos_x' in datos_Pedro)
    assert ('pos_y' in datos_Pedro)
    assert ('damage' in datos_Pedro)

def test_shotting_missile():
    # Robot 1 no hace nada. Robot 2 rota y escanea, dispara.

    robot1_code = """class Juan(Robot):
    def initialize(self):
        self.a="Juan"
    def respond(self):
        pass"""
    robot2_code = """import random 
class Pedro(Robot):
    def initialize(self):
        self.a = "Pedro"
        self.d = 0
        self.s = -1
    def respond(self):
        self.point_scanner(self.d, 10)
        if self.s != -1:
            self.cannon(self.d, self.s)
        else:
            self.d += 10
            self.s = self.scanned()"""
        
    
    twoRobots.setUp(robot1_code, robot2_code)

    setUpUsers()
    token = get_token()
    add_robot('Lucas', 'Juan')
    add_robot('Lucas', 'Pedro')

    url = '?cant_rondas=7500&robots=Juan&robots=Pedro'

    response = client.post("/simulacion" + url, headers = {"Authorization": f"Bearer {token}"})

    twoRobots.tearDown()
    
    simulation_response = response.json()

    assert (response.status_code == 200)

    assert('usuarioGanador' in simulation_response)
    
    assert ('robotGanador' in simulation_response)
    assert (simulation_response['robotGanador'] != 'Juan')

    assert ('robots' in simulation_response)
    assert (simulation_response['robots'] == ['Juan-0', 'Pedro-1'])

    assert ('rondas_robots' in simulation_response)
    assert (len(simulation_response['rondas_robots']) == 2)

    info_rondas_Pedro = simulation_response['rondas_robots']['Pedro-1']
    rondas = len(info_rondas_Pedro)

    assert (rondas <= 7500)

    ronda_n_Pedro = info_rondas_Pedro[rondas-1]

    assert ('is_dead' in ronda_n_Pedro)
    assert (not ronda_n_Pedro['is_dead'])

    assert ('misiles' in ronda_n_Pedro)
    assert (ronda_n_Pedro['misiles'] != [])
    assert (len(ronda_n_Pedro['misiles'][0]) == 3)

    datos_misil = ronda_n_Pedro['misiles'][0]

    assert ('pos_x' in datos_misil)
    assert ('pos_y' in datos_misil)
    assert ('exploto' in datos_misil)

    assert ('datos_robot' in ronda_n_Pedro)
    assert (len(ronda_n_Pedro['datos_robot']) == 3)

    datos_Pedro = ronda_n_Pedro['datos_robot']

    assert ('pos_x' in datos_Pedro)
    assert ('pos_y' in datos_Pedro)
    assert ('damage' in datos_Pedro)
    
def test_bad_robot_name():
    robot1_code = """class Juan(Robot):
    def initialize(self):
        self.a="Juan"
    def respond(self):
        pass"""
    robot2_code = """import random 
class Pedro(Robot):
    def initialize(self):
        self.a = "Pedro"
        self.d = 0
        self.s = -1
    def respond(self):
        self.point_scanner(self.d, 10)
        if self.s != -1:
            self.cannon(self.d, self.s)
        else:
            self.d += 10
            self.s = self.scanned()"""
        
    
    twoRobots.setUp(robot1_code, robot2_code)

    setUpUsers()
    token = get_token()
    add_robot('Lucas', 'Juan')
    add_robot('Lucas', 'Pedro')

    url = '?cant_rondas=500&robots=Loro&robots=Andrea'

    response = client.post("/simulacion" + url, headers = {"Authorization": f"Bearer {token}"})

    twoRobots.tearDown()

    assert (response.status_code == 409)
    assert (response.json() == {'detail' : "Alguno/s de los robots no pertenece al usuario"})

def test_bad_num_rounds():
    robot1_code = """class Juan(Robot):
    def initialize(self):
        self.a="Juan"
    def respond(self):
        pass"""
    robot2_code = """import random 
class Pedro(Robot):
    def initialize(self):
        self.a = "Pedro"
        self.d = 0
        self.s = -1
    def respond(self):
        self.point_scanner(self.d, 10)
        if self.s != -1:
            self.cannon(self.d, self.s)
        else:
            self.d += 10
            self.s = self.scanned()"""
        
    
    twoRobots.setUp(robot1_code, robot2_code)

    setUpUsers()
    token = get_token()
    add_robot('Lucas', 'Juan')
    add_robot('Lucas', 'Pedro')

    url = '?cant_rondas=50&robots=Juan&robots=Pedro'

    response = client.post("/simulacion" + url, headers = {"Authorization": f"Bearer {token}"})

    twoRobots.tearDown()

    assert (response.status_code == 422)
    assert (response.json() == {'detail' : "Numero de rondas no valido"})