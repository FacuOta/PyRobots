
MAX_DISTANCE : int = 700
RELOAD_TIME: int = 3


class Cannon:
    
    direction : int
    distance : int
    is_ready: bool
    missile_list: list
    cannon_reload: int

    def __init__(self):
        self.direction = 0
        self.distance = 0
        self.is_ready = True
        self.missile_list = []
        self.cannon_reload = 0
    
    def get_direction(self) -> int:
        return self.direction
    
    def get_distance(self) -> int:
        return self.distance
    
    def get_state(self) -> bool:
        return self.is_ready
    
    def set_direction(self, direction) -> None:
        self.direction = direction
    
    def set_distance(self, distance) -> None:
        self.distance = min(distance, MAX_DISTANCE)
    
    def set_state(self, state) -> None:
        self.is_ready = state

    def create_missile(self, distance, direction, beg_x, beg_y):
        self.missile_list.append({'distance': distance, 'direction': direction,
        'cur_x': beg_x, 'cur_y': beg_y, 'beg_x': beg_x, 'beg_y': beg_y, 'cur_dist': 0, 'stat': 'flying'})
    
    def reload_cannon(self):
        self.cannon_reload = RELOAD_TIME
        self.set_state(False)
    
    def update_cannon_reload(self):
        if (self.cannon_reload != 0):
            self.cannon_reload -= 1
        if (self.cannon_reload == 0):
            self.set_state(True)
