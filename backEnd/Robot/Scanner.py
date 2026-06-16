
class Scanner:

    scan_result : int
    resolution_in_degree: int
    direction : int

    def __init__(self):
        self.direction = 0
        self.resolution_in_degree = 0
        self.scan_result = -1
    
    def get_direction(self) -> int:
        return self.direction
    
    def get_scan_result(self) -> int:
        return self.scan_result
    
    def get_resolution(self) -> int:
        return self.resolution_in_degree
    
    def set_direction(self, direction) -> None:
        self.direction = direction
    
    def set_distance(self, result) -> None:
        self.scan_result = result

    def set_resolution(self, resolution) -> None:
        self.resolution_in_degree = resolution