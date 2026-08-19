import os
from fastapi import FastAPI, HTTPException, UploadFile, Form, Query, Depends, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from http import HTTPStatus
from fastapi.security import OAuth2PasswordBearer
from crud_handlers import *
from models import *
from helper_functions import *
from pydantic_models import InfoPartida, JSONListPartida, JSONListStrings, MatchResult
from fastapi.staticfiles import StaticFiles
from websocketManager import WebSocketManager
from settings import ORIGENES, preparar_carpetas, ruta
from game_logic import calculate_match

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Las carpetas se crean antes de montarlas: StaticFiles falla si no existen, y
# en el Space /tmp arranca vacío.
preparar_carpetas()

app.mount("/robot_avatars", StaticFiles(directory=ruta("robot_avatars")), name="robot_avatars")
app.mount("/user_avatars", StaticFiles(directory=ruta("user_avatars")), name="user_avatars")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login/")

origins = ORIGENES

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

wsManager = WebSocketManager()


def get_current_user(token: str = Depends(oauth2_scheme)):
    
    user = decode_token(token)
    
    return user


@app.post("/register/")
async def create_user(username: str = Form(), email: str = Form(), password: str = Form(), 
                        avatar: Union[UploadFile, None] = None):

    if avatar:
        if not (check_valid_imagetype(avatar.content_type)):
                raise HTTPException(status_code= HTTPStatus.BAD_REQUEST, detail="Invalid image")
    
    if not (check_password_rules(password)):
       raise HTTPException(status_code= HTTPStatus.BAD_REQUEST, detail="Invalid password")
    
    password_hash = hash_password(password)

    status = add_user(username=username, email = email, password = password_hash)
    if status == "NonUniqueEmailOrUsername":
        raise HTTPException(status_code= HTTPStatus.BAD_REQUEST, detail="Non-unique email or username")
    elif status == "EmailNotValid":
        raise HTTPException(status_code= HTTPStatus.BAD_REQUEST, detail="Invalid email") 
    elif status == "UsernameNotValid":
        raise HTTPException(status_code= HTTPStatus.BAD_REQUEST, detail="Invalid username")
    else:
        if avatar and not testing:
            script_dir = os.path.dirname(__file__)
            # Reemplaza el nombre del archivo por el username, mantiene la extension
            rel_path = ruta('user_avatars', username + os.path.splitext(avatar.filename)[1])
            abs_file_path = os.path.join(script_dir, rel_path)
            contents = await avatar.read()
            f = open(abs_file_path, "wb")
            f.write(contents)
            f.close()

    raise HTTPException(status_code= HTTPStatus.CREATED, detail="User created")


@app.post("/login/", status_code = HTTPStatus.OK)
async def login_user(username: str = Form(), password: str = Form()):
    if not are_valid_credentials(username, password):
        incorrect_username_password()

    user = authenticate_user(username, password)
    
    if not user:
        incorrect_username_password()


    token = create_access_token(data =
        {"username" : user.username, "email" : user.email}
    )

    return {"access_token" : token, "token_type": "bearer"}


@app.get("/users/me", status_code = HTTPStatus.OK)
async def read_users_me(current_user: str = Depends(get_current_user)):
    user = get_user(current_user)

    return {"username" : user.username, "email" : user.email}


@app.get("/partida/list", status_code= HTTPStatus.OK, response_model= JSONListPartida)
async def list_inactive_matches(user: str = Depends(get_current_user)):
    return {'partidas' : matches_list(user, "Inactive")}


@app.get("/partida/list_ended",  status_code= HTTPStatus.OK, response_model= JSONListPartida)
async def list_ended_matches(user: str = Depends(get_current_user)):
    return {'partidas' : matches_list(user, "Ended")}


@app.get("/partida/{match_id}", status_code= HTTPStatus.OK, response_model= InfoPartida)
def match_info(match_id : int, user : str = Depends(get_current_user)):
    if not (verify_match_exists(match_id)):
        raise HTTPException(status_code= HTTPStatus.CONFLICT,
                            detail= f"Match {match_id} doesn't exist")    
    
    return get_match_info(match_id, user)


@app.post("/robot/")
async def create_robot(robotCode: UploadFile, robotName: str = Form(),
                         robotAvatar: Union[UploadFile, None] = None, 
                         current_user: str = Depends(get_current_user)):

    if robotAvatar and not (check_valid_imagetype(robotAvatar.content_type)):
        raise HTTPException(status_code= HTTPStatus.BAD_REQUEST, detail="Invalid image")
    
    status = add_robot(username = current_user, robotName = robotName)
    if status == "RobotNameNotValid":
        raise HTTPException(status_code= HTTPStatus.BAD_REQUEST, detail="Invalid robot name")
    if status == "NonUniqueRobotName":
        raise HTTPException(status_code= HTTPStatus.BAD_REQUEST, detail="Non-unique robot name")
    elif status == 1:
        if not testing:
            script_dir = os.path.dirname(__file__)
            if robotAvatar:
                rel_path = ruta('robot_avatars', current_user + '_' + robotName + os.path.splitext(robotAvatar.filename)[1])
                abs_file_path = os.path.join(script_dir, rel_path)
                contents = await robotAvatar.read()
                f = open(abs_file_path, "wb")
                f.write(contents)
                f.close()

            rel_path = ruta('robot_files', current_user + '_' + robotName + os.path.splitext(robotCode.filename)[1])
            abs_file_path = os.path.join(script_dir, rel_path)
            contents = await robotCode.read()
            g = open(abs_file_path, "wb")
            g.write(contents)
            g.close()

    raise HTTPException(status_code= HTTPStatus.CREATED, detail="Robot created")


@app.post("/crear_partida/", status_code= HTTPStatus.CREATED)
async def crear_partida(nombre_partida : str = Form(), cant_max_players : int = Form(), 
    cant_juegos : int = Form(), cant_rondas : int = Form(), current_user: str = Depends(get_current_user), password: Union[str, None] = Form(None)):
    
    status = guardar_partida(nombre_partida = nombre_partida, cant_max_players = cant_max_players, 
        cant_juegos = cant_juegos, cant_rondas = cant_rondas, creador_username = current_user, password = password )
    if status != 1:
        raise HTTPException(status_code= HTTPStatus.UNAUTHORIZED, detail= status)
    
    ws = get_websocket_address(get_match_id(nombre_partida))

    return {"detail": "Partida Creada", 
            "websocket" : ws}


@app.post("/partida/unirse/", status_code= HTTPStatus.OK)
async def join_match(match_name : str = Form(), robot_name : str = Form(),
                     current_user : str = Depends(get_current_user), password: Union[str, None] = Form(None)):
    
    if not verify_join_info(match_name, robot_name, current_user):
        raise HTTPException(status_code= HTTPStatus.CONFLICT, detail= "El robot o la partida no existen")   #409

    if verify_not_joinable(match_name):
        raise HTTPException(status_code= HTTPStatus.CONFLICT, detail= "La partida esta en proceso o ya ha terminado")
    
    if match_has_password(match_name):
        if not(verify_match_password(match_name, password)):
            raise HTTPException(status_code= HTTPStatus.FORBIDDEN, detail= "Contraseña incorrecta")

    try:
        join_user_to_match(current_user, match_name)
    except Exception as e:
        raise HTTPException(status_code= HTTPStatus.FORBIDDEN, detail= str(e))
    
    join_robot_to_match(current_user, robot_name, match_name)

    lobby = get_match_id(match_name)
    ws = get_websocket_address(lobby)

    await wsManager.broadcast(lobby, {
        "event" : "Union",
        "nombre_usuario" : current_user
    })

    return {"detail" : "Usuario unido a partida",
            "websocket" : ws}


@app.put("/partida/abandonar/", status_code=HTTPStatus.OK)
async def leave_match(match_name : str = Form(), current_user : str = Depends(get_current_user) ):
    p = get_Partida(match_name)

    if not (match_exists(match_name)):
        raise HTTPException(status_code= HTTPStatus.CONFLICT, detail= "Match does not exist")

    if(verify_not_joinable(match_name)):
        raise HTTPException(status_code= HTTPStatus.CONFLICT, detail= "Match is either in progress or has already ended")

    if not (verify_user_is_participating(current_user, match_name)):
        raise HTTPException(status_code= HTTPStatus.CONFLICT, detail= "User is not a player in that match")

    if(verify_user_is_the_creator(current_user, match_name)):
        raise HTTPException(status_code= HTTPStatus.FORBIDDEN, detail= "Creator is not allowed to leave its own match")
    
    remove_user_from_match(current_user, match_name)

    lobby = get_match_id(match_name)

    await wsManager.broadcast(lobby, {
        "event" : "Abandona",
        "nombre_usuario" : current_user
    })

    return {"detail" : "Left the match successfully"}


@app.get("/images", status_code= HTTPStatus.OK)
def images(current_user: str = Depends(get_current_user)):
    lista = []
    for filename in os.listdir(ruta("robot_avatars")):
        if not filename.startswith('.'):
            fullname = filename.split(".")[0]
            username, robotname = fullname.split("_")
            if username == current_user:
                lista.append({
                    'robotname': robotname,
                    "path": "/robot_avatars/" + filename
                })
    
    return lista


@app.get("/get_robots/",status_code= HTTPStatus.OK, response_model=JSONListStrings)
async def getRobots(current_user: str = Depends(get_current_user)):
    return {"robotNames": list_robots(current_user)}


@app.post("/simulacion", status_code= HTTPStatus.OK, response_model= MatchResult)
def run_simulation(cant_rondas : int, current_user: str = Depends(get_current_user), robots: list[str] = Query(default = None)):

    robotsList = list(filter(lambda r: r != '""', robots))

    user_name_list : list[str] = [current_user] * len(robotsList)    
    if not verify_robots(user_name_list ,robotsList):
        raise HTTPException(status_code= HTTPStatus.CONFLICT, detail= "Alguno/s de los robots no pertenece al usuario")       # 409
    
    if cant_rondas < 200 or cant_rondas > 10000:
        raise HTTPException(status_code= HTTPStatus.UNPROCESSABLE_ENTITY, detail= "Numero de rondas no valido")             # 422

    result : MatchResult = calculate_match(user_name_list, robotsList, cant_rondas, 1, True)
    
    return result

@app.put("/partida/iniciar_partida", status_code= HTTPStatus.OK, response_model= MatchResult)
async def run_match(current_user: str = Depends(get_current_user), match_name : str = Form(), creator_robot : str = Form()):

    if not (verify_match_startable(match_name)):
        raise HTTPException(status_code= HTTPStatus.UNPROCESSABLE_ENTITY, detail = "La partida está en progreso, ha terminado o no existe")
    if not (verify_user_is_the_creator(current_user, match_name)):
        raise HTTPException(status_code= HTTPStatus.UNPROCESSABLE_ENTITY, detail = "El usuario no es el creador")
    if not (verify_min_players(match_name)):
        raise HTTPException(status_code= HTTPStatus.UNPROCESSABLE_ENTITY, detail = "No hay suficientes jugadores para iniciar")
    if not (verify_join_info(match_name, creator_robot, current_user)):
        raise HTTPException(status_code= HTTPStatus.UNPROCESSABLE_ENTITY, detail = "El usuario no posee el robot ingresado")

    join_robot_to_match(current_user, creator_robot, match_name)

    lobby = get_match_id(match_name)

    dictInicio = {"event" : "Inicio"}
    await wsManager.broadcast(lobby, dictInicio)

    change_in_progress(match_name, True)

    userList, robotList = list_robots_and_users_in_match(match_name)
    roundCount, gameCount = round_and_game_count(match_name)
    
    result = calculate_match(userList, robotList, roundCount, gameCount, False)
    winnerRobot = result['robotGanador']
    winnerUser = result['usuarioGanador']
    set_winner(winnerUser, match_name)

    dictResult = {"event" : "Finalizado",
            'winnerRobot': winnerRobot,
            'winnerUser': winnerUser}

    await wsManager.broadcast(lobby, dictResult)

    return result

@app.get("/partida/{match_id}/resultados", status_code= HTTPStatus.OK, dependencies=[Depends(get_current_user)])
async def get_match_results(match_id: int):
    if not (verify_match_exists(match_id)):
        return {'detail': 'Partida no existe'}
    if not (verify_match_ended(match_id)):
        return {'detail': 'Partida en progreso o sin iniciar'}

    winnerRobot, winnerUser = get_match_winners(match_id)
    return {'winnerRobot': winnerRobot,
            'winnerUser': winnerUser}


@app.websocket("/lobbys/{lobby_id}")
async def websocket_endpoint(websocket: WebSocket, lobby_id: int):
    await wsManager.connect(lobby_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await wsManager.broadcast(lobby_id, {"Your text": data})
    except:
        wsManager.disconnect(lobby_id, websocket)

@app.get("/users/avatar")
def images(username: str, current_user: User = Depends(get_current_user)):

    for filename in os.listdir(ruta("user_avatars")):
        if not filename.startswith('.'):
            name = filename.split(".")[0]
            if name == username:
                return {
                    "path": "/user_avatars/" + filename
                }
            else:
                return {'detail': 'User has no avatars'}