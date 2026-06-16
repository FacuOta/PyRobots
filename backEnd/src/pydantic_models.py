from typing import Union
from pydantic import BaseModel

class InfoPartida(BaseModel):
    id_partida : int
    nombre_partida : str
    participantes : list[str]
    robots : list[str]
    jugadores_participando : int
    numero_maximo_jugadores : int
    numero_rondas : int
    numero_juegos : int
    fecha_creacion : str
    es_privada : bool
    es_creador : bool
    participa : bool
    termino : bool
    en_progreso : bool
    nombre_ganador : str
    robot_ganador : str
    websocket : str

class JSONListPartida(BaseModel):
    partidas : list[InfoPartida]

class JSONListStrings(BaseModel):
    robotNames: list[str]

class RobotStatus(BaseModel):
    pos_x : int
    pos_y : int
    damage : int

class MissileStatus(BaseModel):
    pos_x : int
    pos_y : int
    exploto : bool

class RoundData(BaseModel):
    is_dead : bool                 # Si esta Vivo o Muerto
    datos_robot : RobotStatus      # Posiciones y vida del Robot
    misiles : list[MissileStatus]  # Misiles disparados por el Robot

class GameData(BaseModel):
    rondas : list[RoundData]      # Informacion de cada Ronda

class MatchResult(BaseModel):
    robotGanador : str
    usuarioGanador: str
    robots : Union[list[str], None] = None                   # Lista de los nombre de los Robots       
    rondas_robots : Union[dict[str, list[RoundData]], None] = None  # Diccionario con key = 'Nombre del Robot' y value = 'Informacion de las rondas del robot'
    
class LobbyEvents(BaseModel):
    event : str
    nombre_usuario : str
