
from Cannon import *
from Motor import *
from Scanner import *

MAX_DEGREE = 360

class Robot:

    pos_x : int
    pos_y : int
    total_damage : int
    is_dead : bool
    scanner : Scanner
    motor : Motor
    weapon : Cannon

    def __init__(self, x : int, y : int):
        self.pos_x = x      # Random
        self.pos_y = y      # Random
        self.total_damage = 0
        self.is_dead = False
        self.motor = Motor()
        self.scanner = Scanner()
        self.weapon = Cannon()
    
    def reset(self):
        self.__init__

    def get_direction(self):
        return self.motor.get_direction()

    def get_velocity(self):
        return self.motor.get_velocity()

    def get_position(self):
        return (self.pos_x, self.pos_y)

    def get_damage(self):
        return self.total_damage

    def is_cannon_ready(self):
        return self.weapon.get_state()

    def cannon(self, degree : int, distance : int):
        
        if distance < 0:
            return

        self.weapon.set_direction(self.__calculate_direction(degree))
        self.weapon.set_distance(distance)

    def point_scanner(self, direction : int, resolution_in_degrees : int):
        self.scanner.set_direction(self.__calculate_direction(direction))
        if resolution_in_degrees < 0:
            resolution_in_degrees = -resolution_in_degrees
        resolution = resolution_in_degrees % 11

        self.scanner.set_resolution(resolution)

    def scanned(self):
        return self.scanner.get_scan_result()

    def drive(self, direction : int, velocity : int):
        if velocity < 0:
            return

        self.motor.set_direction(self.__calculate_direction(direction))
        
        self.motor.set_velocity(velocity)
    
    def __calculate_direction(self, direction):
        if direction < 0:
            new_direction =  (360 + direction) % MAX_DEGREE
        else:
            new_direction = direction % MAX_DEGREE
        
        return new_direction