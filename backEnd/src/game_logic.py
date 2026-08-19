import os
import random
import math
from models import testing
from game_constants import *
from simulation_helpers import *
import sys
sys.path.append('../Robot')
from Robot import *
from settings import ruta

def calculate_match(usernameSet, robotNameSet, roundCount, gameCount, is_simulation):
    filename_list = []
    exec_locals = []
    match_data = {'robotGanador': '',
                    'usuarioGanador': ''}
    
    if is_simulation:
        match_data.update(init_simulation_result(robotNameSet))


    for i in range(len(usernameSet)):
        filename_list.append(usernameSet[i] + '_' + robotNameSet[i] + '.py')
        exec_locals.append(usernameSet[i] + robotNameSet[i])


    script_dir = os.path.dirname(__file__)

    classList = []
    for f in range(len(filename_list)):
        if not testing:
            rel_path = ruta('robot_files', filename_list[f])
        else:
            rel_path = '../tests/test_files/' + filename_list[f]
        abs_file_path = os.path.join(script_dir, rel_path)
        d={}
        exec(open(abs_file_path).read(), globals(), d)
        a = d[robotNameSet[f]](0,0)
        classList.append(a)

    wins_by_robot = []
    for i in range(len(classList)):
        wins_by_robot.append(0)

    for game in range(gameCount):
        remainingRobots = []

        for (i, c) in enumerate(classList, start=0):
            try:
                c.initialize()
            except:
                c.is_dead = True
            
            remainingRobots.append((c, i))
            c.pos_x = random.randint(0, 999)
            c.pos_y = random.randint(0, 999)
        
        for round in range(roundCount):

            remainingRobots = run_round(classList, remainingRobots)

            if is_simulation:
                compile_round_info(classList, match_data['robots'], 
                                    match_data['rondas_robots']
                                   )

            if len(remainingRobots) == 1:
                winner_index = remainingRobots[0][1]
                break
            else:
                if (len(remainingRobots)) == 0 or (round == (roundCount - 1)):
                    winner_index = -1
                    break
        if (winner_index != -1):
            wins_by_robot[winner_index] += 1

    
    wins = max(wins_by_robot)
    winners = [i for i, j in enumerate(wins_by_robot) if j == wins]
    
    if len(winners) == 1:
        champion = wins_by_robot.index(wins)
        match_data['robotGanador'] = robotNameSet[champion]
        match_data['usuarioGanador'] = usernameSet[champion]

    return match_data


def run_round(classList, remainingRobots):
    for c in classList:
        try:
            c.respond()
        except:
            c.is_dead = True
    
    # scan
    for c in classList:
        if c.is_dead:
            continue
        scan_robots(c, classList)

    # attack
    for c in classList:
        if c.is_dead:
            continue
        attack_robots(c, classList)

    # move
    for c in classList:
        if c.is_dead:
           continue
        move_robots(c, classList)

    #check for dead robots
    for c in classList:
        if c.total_damage >= 100:
            c.total_damage = 100
            c.is_dead = True
        if c.is_dead:
            remainingRobots = [i for i in remainingRobots if i[0] != c]
    return remainingRobots

def scan_robots(cur_robot, robots):
    closestDistance = -1
    for r in robots:
        if r.is_dead or r == cur_robot:
            continue
        x = r.pos_x - cur_robot.pos_x
        y = r.pos_y - cur_robot.pos_y
        if (x==0):
            d = 90 if (r.pos_y > cur_robot.pos_y) else 270
        else:
            radians = math.atan2(y,x)
            if radians < 0:
                radians = radians + 2 * math.pi
            d = rad_to_deg(radians) 
            
        robot_dir = cur_robot.scanner.direction
        robot_res = cur_robot.scanner.resolution_in_degree
        if ((robot_dir > robot_res) and (robot_dir < 360 - robot_res)):
            degree = robot_dir
            d1 = d - robot_res
            d2 = d + robot_res
        else:
            degree = robot_dir + 180
            d1 = 180 + d - robot_res
            d2 = 180 + d + robot_res
        if (degree>=d1 and degree <= d2):
            distance = round(math.sqrt((x*x) + (y*y)))
            if (distance < closestDistance or closestDistance == -1):
                closestDistance = distance
                cur_robot.scanner.scan_result = distance


def rad_to_deg(n):
    return (n / math.pi) * 180

def deg_to_rad(n):
    return  (n / 180) * math.pi

def attack_robots(cur_robot, robots):
    dist = cur_robot.weapon.distance
    direct = cur_robot.weapon.direction
    x = cur_robot.pos_x
    y = cur_robot.pos_y
    if (dist != 0 and cur_robot.weapon.get_state()):
        cur_robot.weapon.create_missile(dist, direct, x, y)
        cur_robot.weapon.reload_cannon()
    else:
        cur_robot.weapon.update_cannon_reload()
    
    for mis in cur_robot.weapon.missile_list:
        if mis['stat'] == 'exploding':
            cur_robot.weapon.missile_list.remove(mis)

    for mis in cur_robot.weapon.missile_list:
        if (mis['stat'] == 'flying'):
            mis['cur_dist'] += MIS_SPEED
            if (mis['cur_dist'] > mis['distance']):
                mis['cur_dist'] = mis['distance']
            
            mis['cur_x'] = mis_x = round(mis['beg_x'] + ((mis['cur_dist']) * math.cos(deg_to_rad(mis['direction']))))
            mis['cur_y'] = mis_y = round(mis['beg_y'] + ((mis['cur_dist']) * math.sin(deg_to_rad(mis['direction']))))

            if (mis_x < 0 or mis_x >= BOARD_SIZE or mis_y < 0 or mis_y >= BOARD_SIZE):
                mis['stat'] = 'exploding'

            mis['cur_x'] = mis_x = min(max(mis_x, 0), BOARD_SIZE -1)
            
            mis['cur_y'] = mis_y = min(max(mis_y, 0), BOARD_SIZE -1)
            
            if mis['cur_dist'] == mis['distance']:
                mis['stat'] = 'exploding'
            
            if mis['stat'] == 'exploding':
                for c in robots:
                    if not c.is_dead or c != cur_robot:
                        x_diff = mis_x - c.pos_x
                        y_diff = mis_y - c.pos_y
                        diff_dist =  round(math.sqrt((x_diff**2) + (y_diff**2)))

                        if diff_dist < 5:
                            c.total_damage += 10
                        elif diff_dist < 20:
                            c.total_damage += 5
                        elif diff_dist < 40:
                            c.total_damage += 3

def move_robots(cur_robot, robots):
    
    if (cur_robot.motor.velocity > cur_robot.motor.d_velocity):
        cur_robot.motor.accel -= ACCEL
        if (cur_robot.motor.accel < cur_robot.motor.d_velocity):
            cur_robot.motor.velocity = cur_robot.motor.accel = cur_robot.motor.d_velocity
        else:
            cur_robot.motor.velocity = cur_robot.motor.accel

    elif(cur_robot.motor.velocity < cur_robot.motor.d_velocity):
        cur_robot.motor.accel += ACCEL
        if (cur_robot.motor.accel > cur_robot.motor.d_velocity):
            cur_robot.motor.velocity = cur_robot.motor.accel = cur_robot.motor.d_velocity
        else:
            cur_robot.motor.velocity = cur_robot.motor.accel

    if (cur_robot.motor.direction != cur_robot.motor.d_direction):
        if (cur_robot.motor.velocity <= TURN_SPEED_FACTOR * MAX_VELOCITY):
            cur_robot.motor.direction = cur_robot.motor.d_direction
            cur_robot.motor.range = 0
            cur_robot.motor.org_x = cur_robot.pos_x
            cur_robot.motor.org_y = cur_robot.pos_y
    
    if (cur_robot.motor.velocity > 0):
        cur_robot.motor.range += cur_robot.motor.velocity
        cur_robot.pos_x = calculate_distance_cos(cur_robot.motor.org_x, cur_robot.motor.range, cur_robot.motor.direction)
        cur_robot.pos_y = calculate_distance_sin(cur_robot.motor.org_y, cur_robot.motor.range, cur_robot.motor.direction)
    
    for r in robots:
        if r.is_dead or r == cur_robot:
            continue
        if (r.pos_x == cur_robot.pos_x and r.pos_y == cur_robot.pos_y):
            robot_collision(r)
        
    if (cur_robot.pos_x < 0):
        cur_robot.pos_x = 0
        robot_collision(cur_robot)
    else:
        if (cur_robot.pos_x >= BOARD_SIZE):
            cur_robot.pos_x = BOARD_SIZE - 1
            robot_collision(cur_robot)

    if (cur_robot.pos_y < 0):
        cur_robot.pos_y = 0
        robot_collision(cur_robot)
    else:
        if (cur_robot.pos_y >= BOARD_SIZE):
            cur_robot.pos_y = BOARD_SIZE - 1
            robot_collision(cur_robot)
    pass

def robot_collision(robot):
    robot.motor.velocity = 0
    robot.motor.d_velocity = 0
    robot.total_damage += COLL_DAMAGE

def calculate_distance_cos(beg_x, distance, angle):
    return round(beg_x + (distance * math.cos(deg_to_rad(angle))))


def calculate_distance_sin(beg_y, distance, angle):
    return round(beg_y + (distance * math.sin(deg_to_rad(angle))))
