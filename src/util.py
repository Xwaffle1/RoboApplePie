import os
from cv2 import cv2 as cv
import pyautogui as gui
import numpy as np

# Width and Height of Screen.
width = 1920
height = 1080

user_folder = os.environ['HOMEPATH']
file_path_str = user_folder + "\\CurrentEncounters.txt"

def read_current_battles():
    global file_path_str
    if(not os.path.exists(file_path_str)):
        print("FILE NOT FOUND: " + file_path_str)
        return -1
    else:
        print(file_path_str)
        f = open(file_path_str, "r")
        total_battles = int(f.readline())
        f.close()    
        return total_battles

def update_text_file(total_battles):
    global file_path_str
    f = open(file_path_str, "w")
    f.write(str(total_battles))
    f.close()        

last_position = [None] * 3
def read_player_pos():
    global user_folder, last_position
    position = [None] * 3
    file_path_str = user_folder + "\\PlayerLocation.txt"
    f = open(file_path_str, "r")
    line = f.readline().replace("\n", "")
    split = line.split(', ')
    if(len(split) == 3):
        position[0] = float(split[0])
        position[1] = float(split[1])
        position[2] = float(split[2])
        last_position = position
        return position
    return last_position


def specific_screenshot(bbox):
    global width
    global height

    screenshot = gui.screenshot(region=bbox) 
    screenshot = cv.cvtColor(np.array(screenshot), cv.COLOR_RGB2BGR)
    screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)

    return screenshot

# Gets confidance level of check_for being inside image.
def get_confidance(image, check_for):
    # game_screen = specific_screenshot(((width/2)-100 ,(height/2)+300, 200, 200))
    # template = cv.imread('assets/run_away.png', cv.IMREAD_GRAYSCALE)
    result = cv.matchTemplate(image, check_for, cv.TM_CCOEFF_NORMED)
    max_val = cv.minMaxLoc(result)[1]
    return max_val

def is_Run_On_Screen():
    global width
    global height
    game_screen = specific_screenshot(((width/2)-100 ,(height/2)+300, 200, 200))
    template = cv.imread('assets/run_away.png', cv.IMREAD_GRAYSCALE)
    conf = get_confidance(game_screen, template)
    return conf > 0.8

def is_Trade_On_Screen():
    global width
    global height
    game_screen = specific_screenshot((140,(height/2)+50, 200, 200))
    template = cv.imread('assets/Trade.png', cv.IMREAD_GRAYSCALE)
    conf = get_confidance(game_screen, template)
    return conf > 0.7    

def detect_luma():
    global width
    global height
    found_luma = False
    star_img = cv.imread('assets/star_background.png')
    game2gray = specific_screenshot((width - 300, 0, 200, 400))
    star2gray = cv.cvtColor(star_img, cv.COLOR_BGR2GRAY)

    result = cv.matchTemplate(game2gray, star2gray, cv.TM_CCOEFF_NORMED)

    # get best max positions
    max_val = cv.minMaxLoc(result)[1]

    # print('Best Match loc: %s' % str(max_loc))
    print('Best Match confidence: %s'    % str(max_val))
    

    if(max_val > 0.7):
        found_luma = True
        print("FOUND LUMA")
    return found_luma    