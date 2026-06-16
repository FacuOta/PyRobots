import sys
sys.path.append('../src')
from game_logic import *
sys.path.append('../Robot')
from Robot import *
from Motor import MAX_VELOCITY
from game_constants import *
import unittest

class twoRobots(unittest.TestCase):
    def setUp(robot1_code, robot2_code):
        file_string1 = "test_files/Fran_Juan.py"
        file_string2 = "test_files/Jose_Pedro.py"
        f = open(file_string1, "w")
        f.write(robot1_code)
        f.close()
        g = open(file_string2, "w")
        g.write(robot2_code)
        g.close()

    def tearDown():
        os.remove("test_files/Fran_Juan.py")
        os.remove("test_files/Jose_Pedro.py")
        
def test_still_robot():
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
    result = calculate_match(["Fran", "Jose"], ["Juan", "Pedro"], 20, 1, False)
    twoRobots.tearDown()


    assert (result['robotGanador'] == '') # Ninguno de los robots de la lista gano

def test_bottom_crash_robot():
    # Robot 2 se choca continuamente contra la pared de abajo. Gana Robot 1

    robot1_code = """class Juan(Robot):
    def initialize(self):
        pass
    def respond(self):
        pass"""
    robot2_code = """class Pedro(Robot):
    def initialize(self):
        pass
    def respond(self):
        self.drive(270, 30)"""
    
    twoRobots.setUp(robot1_code, robot2_code)
    # Dada cualquier posicion, tardara como minimo BOARD_SIZE/MAX_VELOCITY en llegar al borde
    # y 100/COLL_DAMAGE en morir siendo que está en el borde. Tener en cuenta tambien la aceleracion
    minimum_round = BOARD_SIZE//MAX_VELOCITY + 100//COLL_DAMAGE + MAX_VELOCITY//ACCEL

    result = calculate_match(["Fran", "Jose"], ["Juan", "Pedro"], minimum_round, 1, False)
    twoRobots.tearDown
    assert (result['robotGanador'] == "Juan") # Gano el robot 1 (posicion 0 en el arreglo)

def test_top_crash_robot():
    # Robot 1 se choca continuamente contra la pared de arriba. Gana Robot 2


    robot1_code = """class Juan(Robot):
    def initialize(self):
        pass
    def respond(self):
        self.drive(90, 30)"""
    robot2_code = """class Pedro(Robot):
    def initialize(self):
        pass
    def respond(self):
        pass"""
    
    twoRobots.setUp(robot1_code, robot2_code)
    minimum_round = BOARD_SIZE//MAX_VELOCITY + 100//COLL_DAMAGE + MAX_VELOCITY//ACCEL
    
    result = calculate_match(["Fran", "Jose"], ["Juan", "Pedro"], minimum_round, 1, False)
    twoRobots.tearDown()
    assert (result['robotGanador'] == 'Pedro') # Gano el robot 2 (posicion 1 en el arreglo)

def test_right_crash_robot():
    # Robot 1 se choca continuamente contra la pared de la derecha. Gana Robot 2


    robot1_code = """class Juan(Robot):
    def initialize(self):
        pass
    def respond(self):
        self.drive(0, 30)"""
    robot2_code = """class Pedro(Robot):
    def initialize(self):
        pass
    def respond(self):
        pass"""
    
    twoRobots.setUp(robot1_code, robot2_code)
    minimum_round = BOARD_SIZE//MAX_VELOCITY + 100//COLL_DAMAGE + MAX_VELOCITY//ACCEL
    
    result = calculate_match(["Fran", "Jose"], ["Juan", "Pedro"], minimum_round, 1, False)
    twoRobots.tearDown()
    assert (result['robotGanador'] == 'Pedro') # Gano el robot 2 (posicion 1 en el arreglo)

def test_left_crash_robot():
    # Robot 2 se choca continuamente contra la pared de la izquierda. Gana Robot 1


    robot1_code = """class Juan(Robot):
    def initialize(self):
        pass
    def respond(self):
        pass"""
    robot2_code = """class Pedro(Robot):
    def initialize(self):
        pass
    def respond(self):
        self.drive(180, 30)"""
    
    twoRobots.setUp(robot1_code, robot2_code)
    minimum_round = BOARD_SIZE//MAX_VELOCITY + 100//COLL_DAMAGE + MAX_VELOCITY//ACCEL
    
    result = calculate_match(["Fran", "Jose"], ["Juan", "Pedro"], minimum_round, 1, False)
    twoRobots.tearDown()
    assert (result['robotGanador'] == 'Juan') # Gano el robot 1 (posicion 0 en el arreglo)

def test_missile():
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
        self.point_scanner(self.d, 1)
        if self.s != -1:
            self.cannon(self.d, self.s)
        else:
            self.d += 1
            self.s = self.scanned()"""
        
    
    twoRobots.setUp(robot1_code, robot2_code)
    rounds = 400
    wins_first_robot = 0
    wins_second_robot = 0
    draws = 0
    for i in range(50):
        result = calculate_match(["Fran", "Jose"], ["Juan", "Pedro"], rounds, 1, False)
        if (result['robotGanador'] == 'Pedro'):
            wins_first_robot+=1
        elif (result['robotGanador'] == 'Juan'):
            wins_second_robot+=1
        else:
            draws+=1
    twoRobots.tearDown()
    assert (wins_first_robot>1 and wins_second_robot == 0) # Nunca gana el segundo robot. 
    # El primer bot gana a veces, pero no siempre, ya que no se mueve y los misiles tienen rango limitado

def test_cos():
    x = calculate_distance_cos(200, 100, 0)
    assert(x == 300)
def test_sin():
    y = calculate_distance_sin(200, 100, 90)
    assert(y == 300)
