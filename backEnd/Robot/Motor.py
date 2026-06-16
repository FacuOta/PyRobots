
MAX_VELOCITY : int = 20


class Motor:
    
    direction : int
    velocity : int
    d_direction: int
    d_velocity: int
    accel: int
    range: int
    org_x: int
    org_y: int

    def __init__(self):
        self.direction = 0
        self.velocity = 0
        self.d_direction = 0
        self.d_velocity = 0
        self.accel = 0
        self.range = 0
        self.org_x = 0
        self.org_y = 0

    def get_direction(self):
        return self.direction
    
    def get_velocity(self):
        return self.velocity
    
    def set_direction(self, direction):
        self.d_direction = direction
    
    def set_velocity(self, velocity):
        if velocity > MAX_VELOCITY:
            self.d_velocity = MAX_VELOCITY
        else:
            self.d_velocity = velocity
