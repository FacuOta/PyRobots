from pony.orm import *
from db_creation import *
from configparser import *
import os
import random

config = RawConfigParser()
config.read(os.path.join(os.path.dirname(__file__),'config.ini'))
testing = config['DATABASE'].getboolean('testing')
db = create_db(testing)

class User(db.Entity):
    username = Required(str, unique=True)
    email = Required(str, unique=True)
    password = Required(str)
    is_verified = Required(bool, default = False)
    partidas_unidas = Set('Partida', reverse='Participan')
    verif_code = Required(int)
    partidas_Creadas = Set('Partida', reverse='Creador')
    cant_ganadas = Required(int, default=0, unsigned=True)
    cant_perdidas = Required(int, default=0, unsigned=True)
    robots = Set('Robot')

class Robot(db.Entity):
    user = Required('User')
    partidas = Set('Partida')
    nombre = Required(str)
    PrimaryKey(user, nombre)
    cant_ganadas = Required(int, default=0, unsigned=True)
    partidas_ganadas = Set('Partida', reverse='ganador')

class Partida(db.Entity):
    id = PrimaryKey(int, auto=True)
    Participan = Set('User', reverse='partidas_unidas')
    Creador = Required('User', reverse='partidas_Creadas')
    robots = Set('Robot')
    nombre_partida = Required(str)
    cant_rondas = Required(int, unsigned=True)
    cant_juegos = Required(int, unsigned=True)
    cant_max_players = Required(int, unsigned=True)
    en_progreso = Required(bool, default = False)
    has_ended = Required(bool, default = False)
    date_time = Required(str)
    password = Optional(str,16)
    ganador = Optional('Robot', reverse = 'partidas_ganadas')

db.generate_mapping(create_tables= True)
