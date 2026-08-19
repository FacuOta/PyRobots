from pony.orm import *
from email_validator import validate_email, EmailNotValidError
from models import *
from helper_functions import *
from typing import Union
from datetime import datetime as dt

@db_session
def add_user(username, email, password):
    # Si el email es valido, la password es valida y el usuario no existe en la bd, se crea
    try:
        emailObject = validate_email(email)
        email = emailObject.email
        
        if not (check_valid_username(username)):
            return "UsernameNotValid"

        if not User.exists(lambda user: user.username == username or user.email == email):
            User(username = username, email = email, password = password, verif_code = random.randrange(100,999999), is_verified = True)
            return 1
        else:
            return "NonUniqueEmailOrUsername"
    except EmailNotValidError as errorMsg:
        return "EmailNotValid"


@db_session
def authenticate_user(username: str, password: str):
    user : User = get_user(username)

    if not user:
        return False

    if not verify_password(password, user.password):
        return False

    return user


@db_session
def get_user(username : str):
    return User.get(username = username)


@db_session
def get_robot(username : str, robot_name : str):
    user = get_user(username)
    return Robot.get(user = user, nombre = robot_name)

@db_session
def get_match(match_name : str):
    return Partida.get(nombre_partida = match_name)


@db_session
def get_Partida(match_name : str):
    return Partida.get(nombre_partida = match_name)


@db_session
def inactive_matches():
    return select(p for p in Partida
                    if(not (p.en_progreso or p.has_ended)))[:]


@db_session
def ended_matches():
    return select(p for p in Partida if p.has_ended)[:]


@db_session
def compile_match_info(match: Partida, current_user: User):
    users = list(map(lambda u: u.username, match.Participan))
    robots = list(map(lambda r: r.nombre, match.robots))

    if testing:
        users.sort()
        robots.sort()

    rGanador, uGanador = get_match_winners(match.id)

    return {
        "id_partida": match.id,
        "nombre_partida" : match.nombre_partida,
        "participantes" : users,
        "robots" : robots,
        "jugadores_participando" : len(match.Participan),
        "numero_rondas" :  match.cant_rondas,
        "numero_juegos" : match.cant_juegos,
        "numero_maximo_jugadores" : match.cant_max_players,
        "fecha_creacion" : match.date_time,
        "es_privada" :  match.password != '',
        "es_creador" : current_user == match.Creador,
        "participa" : current_user in match.Participan,
        "termino" : verify_match_ended(match.id),
        "en_progreso" : verify_match_in_progress(match.id),
        "nombre_ganador" : uGanador,
        "robot_ganador" : rGanador,
        "websocket" : get_websocket_address(match.id)
    }


@db_session
def get_match_info(match_id : int, username : str):
    match = Partida.get(id = match_id)
    user = get_user(username)

    return compile_match_info(match, user)


@db_session
def matches_list(username: str, match_type: str):
    queries = {"Inactive": inactive_matches,
               "Ended" : ended_matches
              }
    
    query = queries[match_type]

    matches = query()
    matchList = []

    current_user = get_user(username)

    for match in matches:
        matchList.append(
            compile_match_info(match, current_user)
        )
    
    return matchList


@db_session
def add_robot(username, robotName):
    if len(robotName)> 16:
        return "RobotNameNotValid"
    
    userObj = User.get(username = username)

    if not Robot.exists(lambda robot: robot.nombre == robotName and robot.user.id == userObj.id):
        Robot(user = userObj, nombre = robotName)
        rob  = Robot.get(user = userObj, nombre = robotName)
        userObj.robots.add(rob)
        return 1
    else:
        return "NonUniqueRobotName"


@db_session
def guardar_partida(nombre_partida : str, cant_max_players : int, cant_juegos : int, 
                cant_rondas : int, creador_username : str, password : Union[str, None] = None):

    creador = get_user(creador_username)

    if (cant_max_players > 4 or cant_max_players < 2) :
        return "cant_max_player_NotValid"
    if (cant_juegos >= 200 or cant_juegos < 1):
        return "cant_juegos_NotValid"
    if (cant_rondas >= 10000 or cant_rondas < 200):
        return "cant_rondas_NotValid"
    if (exists(p for p in Partida if p.nombre_partida == nombre_partida)):
        return "Nombre de partida no valido"
    if (password):
        if not (check_password_rules(str(password))):
            return "PasswordNotValid"
        p = Partida(nombre_partida = nombre_partida, Creador= creador.id,  cant_rondas = cant_rondas, cant_juegos = cant_juegos, 
            cant_max_players = cant_max_players, password = password, date_time = dt.now().isoformat(' '))
    else:
        p = Partida(nombre_partida = nombre_partida, Creador= creador.id,  cant_rondas = cant_rondas, cant_juegos = cant_juegos, 
            cant_max_players = cant_max_players, date_time = dt.now().isoformat(' '))

    commit()
    
    join_user_to_match(creador_username, nombre_partida)
    return 1


@db_session
def join_user_to_match(username : str, match_name : str):
    user : User = get_user(username)
    partida : Partida = Partida.get(nombre_partida = match_name)

    if(user in partida.Participan):
        raise Exception("Ya esta unido a la partida")
    if len(partida.Participan) == partida.cant_max_players:
        raise Exception("La partida esta llena")  
        
    partida.Participan.add(user)


@db_session
def remove_user_from_match(username : str, match_name : str):
    p = get_Partida(match_name)
    user = get_user(username)
    p.Participan.remove(user)

    # Eliminar los robots que haya agregado
    robots = Robot.get(lambda r: r.user == user and r in p.robots)
    p.robots.remove(robots)


@db_session
def join_robot_to_match(username : str, robot_name : str, match_name : str):
    robot : Robot = get_robot(username, robot_name)

    partida : Partida = Partida.get(nombre_partida = match_name)

    partida.robots.add(robot)


@db_session
def confirm_user(usuario : str):
    p = User.get(username = usuario)
    p.set(is_verified = True)
    p.set(verif_code = 0)


@db_session
def list_robots(username: str):
    robotList = []
    lista = []

    user = get_user(username)

    lista = user.robots.select()[:]

    for m in lista:
        robotList.append(m.nombre)
    return robotList


@db_session
def get_match_id(match_name : str):
    p : Partida = Partida.get(nombre_partida = match_name)
    return p.id


@db_session
def verify_join_info(match_name : str, robot_name : str, username : str):
    user : User = get_user(username)
    robot : Robot = get_robot(username, robot_name)
    
    robot_exists = robot in user.robots

    return match_exists(match_name) and robot_exists


@db_session 
def match_exists(match_name : str):
    return exists(p for p in Partida if p.nombre_partida == match_name)


@db_session
def verify_user_is_participating(username : str, match_name : str):
    p = Partida.get(nombre_partida = match_name)
    current_user = User.get(username = username)
    return current_user in p.Participan


@db_session 
def verify_user_is_the_creator(username : str, match_name : str):
    p = Partida.get(nombre_partida = match_name)
    current_user = User.get(username = username)
    return current_user == p.Creador


@db_session
def verify_not_joinable(match : str):
    p = Partida.get(nombre_partida = match)
    return p.has_ended | p.en_progreso


@db_session
def verify_match_password(match_name: str, password: Union[str, None]):
    p = Partida.get(nombre_partida = match_name)

    return (password == p.password)


@db_session
def match_has_password(match_name: str):
    p = Partida.get(nombre_partida = match_name)
    return (p.password)


@db_session
def change_in_progress(match : str, progress : bool):
    p = Partida.get(nombre_partida = match)
    p.set(en_progreso = progress)


@db_session
def change_has_ended(match : str, status : bool):
    p = Partida.get(nombre_partida = match)
    p.set(has_ended = status)


@db_session
def verify_robots(users : list[str], robots : list[str]):
    exists = True
    
    for i in range(len(users)):
        user : User = get_user(users[i])
        robot : Robot = get_robot(users[i], robots[i])

        exists &= robot in user.robots

    return exists


@db_session
def verify_min_players(match_name: str):
    p = get_Partida(match_name)
    return len(p.Participan)>=2


@db_session
def list_robots_and_users_in_match(match_name: str):
    p = get_Partida(match_name)
    robotNameList = []
    userNameList = []
    
    robotList =  p.robots.select()[:]
    for u in p.Participan:
        robot = [x for x in robotList if x.user.username == u.username][0]
        robotNameList.append(robot.nombre)
        userNameList.append(u.username)

    return userNameList, robotNameList


@db_session
def round_and_game_count(match_name: str):
    p = get_Partida(match_name)

    return p.cant_rondas, p.cant_juegos


@db_session
def set_winner(winnerUser: str, match_name: str):
    p = get_Partida(match_name)
    if (winnerUser != ''):
        u = get_user(winnerUser)
        rList = p.robots.select()[:]
        r = [x for x in rList if x.user.username == u.username][0]
        p.set(ganador = r, en_progreso = False, has_ended = True)
        r.cant_ganadas += 1
        r.partidas_ganadas.add(p)
    else:
        p.set(en_progreso = False, has_ended = True)


@db_session
def verify_match_startable(match_name: str):
    p = get_Partida(match_name)
    return (p != None) and (not p.has_ended) and (not p.en_progreso)


@db_session
def get_match_winners(match_id: int):
    p = Partida.get(id = match_id)

    robotTemp = p.ganador
    if (p.ganador == None):
        robot = ''
        user = ''
    else:
        user = robotTemp.user.username
        robot = robotTemp.nombre
    return robot, user


@db_session
def verify_match_exists(match_id: int):
    return exists(p for p in Partida if p.id == match_id)


@db_session
def verify_match_ended(match_id: int):
    p = Partida.get(id = match_id)

    return p.has_ended


@db_session
def verify_match_in_progress(match_id: int):
    p = Partida.get(id = match_id)

    return p.en_progreso