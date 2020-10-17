from cv2 import cv2 as cv
import numpy as np
import os
import random
import copy
from time import sleep
from time import time
import win32gui 
from PIL import ImageGrab
import pyautogui as gui
from pyautogui import press, typewrite, hotkey
import threading
import boto3

# Current State of Bot.
STATE = 'Walk'
# Whether the bot detected a luma.
found_luma = False
current_dir = 0
total_battles = 0
# Width and Height of Screen.
width = 1920
height = 1080
# Whether the bot should capture the TemTem for you.
catch = False
x = 0
y = 0
file_path_str = None

print('WALKING...')
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

def press_key(keys, milliseconds):
    start = time()
    
    while True:
        for key in keys:
            gui.keyDown(key)
        if time() > (start + milliseconds/1000):
            for key in keys:
                gui.keyUp(key)
            break
def walk():
    global current_dir
    seconds = random.randint(200, 500)
    direction_int = random.randint(0, 1)
    if current_dir == 0:
        current_dir = 1
        press_key(['d'], seconds)
    elif current_dir == 1:
        current_dir = 0
        press_key(['a'], seconds)
    # elif direction_int == 2:
    #     press_key(['s'], seconds)
    # elif direction_int == 3:
    #     press_key(['d'], seconds)
    # elif direction_int == 4:
    #     press_key(['w', 'a'], seconds)
    # elif direction_int == 5:
    #     press_key(['w', 'd'], seconds)
    # elif direction_int == 6:
    #     press_key(['s', 'd'], seconds)
    # elif direction_int == 7:
    #     press_key(['a', 'd'], seconds)            
    # press('enter')    

def walk_circle():
    gui.keyDown('w')
    sleep(.03/1000)
    gui.keyDown('a')    
    gui.keyUp('w')
    sleep(.03/1000)       
    gui.keyDown('s')
    gui.keyUp('a')        
    sleep(.03/1000)
    gui.keyDown('d')    
    gui.keyUp('s')    
    sleep(.04/1000)
    gui.keyUp('d')
    gui.keyDown('w')
    sleep(.005/1000)
    gui.keyUp('w')
    

offset = 0
left = 0
def walk_line():
    global offset, left, x, y
    total_time = random.randint(1000,1500)
    per_stroke = total_time / 4
    adjusted_stroke = per_stroke

    if offset == 0 and random.randint(1,100) < 33:
        offset = random.randint(100, 200)
        # print(str(offset))

    if offset != 0:
        adjusted_stroke = per_stroke + ((offset / 2)*-1)
        # print(str(adjusted_stroke))88

    if left == 1:
        left = 0
        gui.keyDown('a')    
        sleep(adjusted_stroke / 1000)
        gui.keyDown('d')    
        gui.keyUp('a')
        sleep(per_stroke / 1000)       
        gui.keyDown('a')
        gui.keyUp('d')        
        sleep(per_stroke / 1000)
        gui.keyDown('d')    
        gui.keyUp('a')    
        sleep(adjusted_stroke / 1000)
        gui.keyUp('d')
        gui.keyUp('a')
    else:
        left = 1
        gui.keyDown('d')
        sleep(adjusted_stroke / 1000)
        gui.keyDown('a')    
        gui.keyUp('d')
        sleep(per_stroke / 1000)       
        gui.keyDown('d')
        gui.keyUp('a')        
        sleep(per_stroke / 1000)
        gui.keyDown('a')    
        gui.keyUp('d')    
        sleep(adjusted_stroke / 1000)
        gui.keyUp('a')
        gui.keyUp('d')

    if offset != 0:
        offset = 0

def is_Temtem_On_Screen():
    is_on_screen = True
    game_screen = gui.screenshot() 
    game_screen = cv.cvtColor(np.array(game_screen), cv.COLOR_RGB2BGR)
    game_screen = cv.cvtColor(game_screen, cv.COLOR_BGR2GRAY)
    early_access_image = cv.imread('assets/TemTemEarlyAccess.png', cv.IMREAD_GRAYSCALE)
    result = cv.matchTemplate(game_screen, early_access_image, cv.TM_CCOEFF_NORMED)
    
    # get best max positions
    max_val = cv.minMaxLoc(result)[1]

    if max_val <= 0.53:
        is_on_screen = False

    # if max_val > 0.53:
    #     print("FOUND TemTem Text")
    #     # Show Result.
    #     # star_width = early_access_image.shape[1]
    #     # star_height = early_access_image.shape[0]
    #     # top_left = max_loc
    #     # botom_right = (top_left[0] + star_width, top_left[1] + star_height)
    #     # cv.rectangle(game_screen, top_left, botom_right, color=(0,255,255), thickness = 2, lineType = cv.LINE_4)
    #     # cv.imshow('TemTemText?', game_screen)
    # else:
    #     is_on_screen = False
        # print('NOT ON SCREEN..')

    return is_on_screen
    
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
    
def use_tem_card():
    sleep(random.randint(100,300)/1000)
    press('7')
    sleep(random.randint(100,300)/1000)
    press('e')
    sleep(random.randint(100,300)/1000)
    press('f')

def update_text_file():
    global total_battles
    f = open(file_path_str, "w")
    f.write(str(total_battles))
    f.close()

def take_action():
    global STATE
    global total_battles
    global catch
    if STATE == 'Walk':
        on_screen = is_Trade_On_Screen()
        if on_screen:            
            walk_line()
            if(random.randint(0,2) == 1):
                walk_circle()
        else:
            STATE = 'Battle Started'            
    elif STATE == 'Battle Started':
        while(not is_Run_On_Screen()):
            print('Waiting...')
            sleep(1)
        print(STATE)
        sleep(1)
        STATE = 'Detect Luma'
    elif STATE == 'Detect Luma':
        found_luma = detect_luma()
        print(STATE)
        if found_luma:
            STATE = 'FOUND LUMA'
            send_text()
            if catch:
                STATE = 'CAPTURE'
        else:
            STATE = 'Run Away'    
    elif STATE == 'Run Away':       
        print(STATE)
        while(is_Run_On_Screen()):
            press('8')
            press('8')
            sleep(1/8)
        print('RAN AWAY')
        total_battles += 1
        update_text_file()
        STATE = 'Walk'
        while(not is_Trade_On_Screen()):
            sleep(1/8)
        print('Total Encounters: ' + str(total_battles))
    elif STATE == 'FOUND LUMA':
        sleep(30)
        print('Total Encounters: ' + str(total_battles))
    elif STATE == 'CAPTURE':
        if is_Run_On_Screen():
            use_tem_card()

def take_screenshot():
    screenshot = gui.screenshot() 
    screenshot = cv.cvtColor(np.array(screenshot), cv.COLOR_RGB2BGR)
    return screenshot

def send_text():
    global total_battles
    ACCESS_KEY = ''
    SECRET_KEY = ''
    sns = boto3.client(
        'sns',
         region_name='us-east-1',
         aws_access_key_id=ACCESS_KEY,
         aws_secret_access_key=SECRET_KEY
    )
    # Send a SMS message to the specified phone number
    response = sns.publish(
        TopicArn='arn:aws:sns:us-east-1:896080545390:TemTem_ApplePie',    
        Message=' A wild Luma has appeared! It took ' + str(total_battles) + ' encounters. ',    
    )

    # Print out the response
    print(response)    

def main():

    global width
    global height
    global file_path_str
    global total_battles

    user_folder = os.environ['HOMEPATH']
    file_path_str = user_folder + "\\CurrentEncounters.txt"

    if(not os.path.exists(file_path_str)):
        print("FILE NOT FOUND: " + file_path_str)
        return
    else:
        print(file_path_str)
        f = open(file_path_str, "r")
        total_battles = int(f.readline())
        print("BOT STARTED WITH: " + str(total_battles) + " battles")
        f.close()

    last_mouse_move = time()
    while(True):
        active_window = gui.getActiveWindow()    
        if active_window != None and active_window.title == 'Temtem':
            take_action()
            if last_mouse_move + random.randint(10,20) < time():
                last_mouse_move = time()
                if(random.randint(0, 100) < 10):
                    gui.moveTo(width/2 + random.randint(-500,200), random.randint(100,400), duration=(random.randint(1,2) * random.random()))
                    gui.leftClick()

        else:
            print('TemTem not opened..')
            sleep(2)

        # if(STATE != 'Walk'):
            # print('Loop took ' + str(time() - loop_time))        
        # loop_time = time()

if __name__ == "__main__":
    main()