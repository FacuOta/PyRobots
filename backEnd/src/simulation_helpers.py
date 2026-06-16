from pydantic_models import GameData
import sys
sys.path.append('../Robot')
from Robot import *

def set_robot_names(robotNames: list[str]):
    names = []

    for i in range(len(robotNames)):
        names.append(robotNames[i] + f"-{i}")
    
    return names

def init_simulation_result(robotNameList : list[str]):
    robotNames = set_robot_names(robotNameList)
    
    simulation_data = {
        'robots' : robotNames,
        'rondas_robots' : dict()
    }

    for rName in robotNames:
        simulation_data['rondas_robots'][rName] = []

    return simulation_data

def compile_round_info(robots, robots_name : list[str], robots_rounds : dict[str, GameData]):
    for i in range(len(robots)):
        RoundData = {
            'is_dead' : robots[i].is_dead,
            'datos_robot' : {
                'pos_x' : robots[i].pos_x,
                'pos_y' : robots[i].pos_y,
                'damage' : robots[i].total_damage
            },
            'misiles' : []
        }
        for missile in robots[i].weapon.missile_list:
            MissileStatus = {
                'pos_x' : missile['cur_x'],
                'pos_y' : missile['cur_y'],
                'exploto' : missile['stat'] == 'exploding'
            }
            RoundData['misiles'].append(MissileStatus)

        nombre_robot = robots_name[i]

        robots_rounds[nombre_robot].append(RoundData)