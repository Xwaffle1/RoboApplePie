import random
import pyautogui as gui
from time import time
from math import cos, sin, pi
from util import read_current_battles, read_player_pos, is_Trade_On_Screen

radius_x = 2
radius_y = 4
position = [None] * 3
origin = [None] * 3
ai_STATE = 'Walk'

def get_possible_dir(ms):
    global origin, radius_x, radius_y, position
    chars = []
    x = position[0] 
    z = position[2]

    if x - 1 >= origin[0] - radius_x:
        chars.append('a')
        
    if x + 1 <= origin[0] + radius_x:
        chars.append('d')

    if z - 1 >= origin[2] - radius_y:
        chars.append('s')

    if z + 1 <= origin[2] + radius_y:
        chars.append('w')

    # if x - ms >= -radius and y + ms <= radius:
    #     chars.append('aw')

    # if x - ms >= -radius and y - ms >= -radius:
    #     chars.append('as')

    # if x + ms <= radius and y + ms <= radius:
    #     chars.append('dw')

    # if x + ms <= radius and y - ms >= -radius:
    #     chars.append('ds')        

    return chars

def player_in_area():
    global origin, position, radius_x, radius_y

    # print(origin)
    # print(position)
    # print(radius)
    
    if position == None:
        return False

    origin_x = origin[0]
    origin_z = origin[2]

    pos_x = position[0]
    pos_z = position[2]
    in_area = pos_x > origin_x - radius_x and pos_x < origin_x + radius_x and pos_z > origin_z - radius_y and pos_z < origin_z + radius_y
    if not in_area:
        print("NOT IN AREA.")
    return in_area

def walk(origin_param, position_param):
    global origin, position
    origin = origin_param
    position = position_param
    milliseconds = 10 * random.randint(20, 50)
    keys = get_possible_dir(milliseconds)
    print(keys)
    rand = random.randint(0, len(keys)-1)
    keys_to_press = list(keys[rand])
    press_key(keys_to_press, milliseconds)

def press_key(keys, milliseconds):
    start = time()
    for key in keys:
        gui.keyDown(key)
    while True and player_in_area():
        if time() > (start + milliseconds / 1000):        
            break
        
    for key in keys:
        gui.keyUp(key)

def walk_to(x, z):
    global position
    position = read_player_pos()
    if(position == None):
        return
    x_diff = abs(abs(position[0]) - abs(x))
    z_diff = abs(abs(position[2]) - abs(z))

    w = False
    a = False
    s = False
    d = False
    while (x_diff > 0.5 or z_diff > 0.5) and is_Trade_On_Screen():
        # print(str(x_diff) + ", " + str(z_diff))
        # print(str(position[0]) + ", " + str(position[2]) + " -> " + str(x) + ", " + str(z))
        if position[0] < x:
            if a or not d:
                a = False
                d = True
                gui.keyUp('a')
                gui.keyDown('d')            
        elif position[0] > x:
            if d or not a:
                d = False
                a = True
                gui.keyUp('d')
                gui.keyDown('a')

        if position[2] < z:
            if s or not w:
                s = False
                w = True
                gui.keyUp('s')
                gui.keyDown('w')    
        elif position[2] > z:
            if w or not s:
                w = False
                s = True
                gui.keyUp('w')
                gui.keyDown('s')    

        position = read_player_pos()
        x_diff = abs(abs(position[0]) - abs(x))
        z_diff = abs(abs(position[2]) - abs(z))

    
    for key in ['w', 'a', 's', 'd']:
        gui.keyUp(key)

# position = read_player_pos()
# origin = position.copy()

# while True:
#     walk_to(origin[0] + random.randint(-1, 1), origin[2] + random.randint(0, 4))
