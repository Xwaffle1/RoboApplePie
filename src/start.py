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
# Most Recent Screenshot taken.
screenshot = None 
# Whether the bot detected a luma.
found_luma = False

current_dir = 0

total_battles = 0

print('WALKING...')
def detect_luma(game_img):
    found_luma = False
    star_img = cv.imread('assets/star_background.png')

    game2gray = cv.cvtColor(game_img, cv.COLOR_BGR2GRAY)
    star2gray = cv.cvtColor(star_img, cv.COLOR_BGR2GRAY)

    result = cv.matchTemplate(game2gray, star2gray, cv.TM_CCOEFF_NORMED)

    # get best max positions
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

    # print('Best Match loc: %s' % str(max_loc))
    print('Best Match confidence: %s'    % str(max_val))
    

    if(max_val > 0.7):
        found_luma = True
        print("FOUND LUMA")
            # Show Result.
        star_width = star_img.shape[1]
        star_height = star_img.shape[0]

        top_left = max_loc
        botom_right = (top_left[0] + star_width, top_left[1] + star_height)

        cv.rectangle(game_img, top_left, botom_right, color=(0,255,255), thickness = 2, lineType = cv.LINE_4)
    return found_luma

def get_game_window(name):
    # Get All Open Windows.
    windows_list = []
    toplist = []
    def enum_win(hwnd, result):
        win_text = win32gui.GetWindowText(hwnd)
        windows_list.append((hwnd, win_text))
    win32gui.EnumWindows(enum_win, toplist)
    game_hwnd = 0
    for (hwnd, win_text) in windows_list:
        if name in win_text:
            game_hwnd = hwnd

    return game_hwnd

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

    sleep(.020/1000)       
    gui.keyDown('s')
    gui.keyUp('a')        
    sleep(.001/1000)
    gui.keyDown('d')    
    gui.keyUp('s')    
    sleep(.025/1000)
    gui.keyUp('d')
    

offset = 0
left = 0
def walk_line():
    global offset
    global left
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
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

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

def is_Trade_On_Screen():
    is_on_screen = True
    game_screen = gui.screenshot() 
    game_screen = cv.cvtColor(np.array(game_screen), cv.COLOR_RGB2BGR)
    game_screen = cv.cvtColor(game_screen, cv.COLOR_BGR2GRAY)
    early_access_image = cv.imread('assets/Trade.png', cv.IMREAD_GRAYSCALE)
    result = cv.matchTemplate(game_screen, early_access_image, cv.TM_CCOEFF_NORMED)
    
    # get best max positions
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

    # print(str(max_val) + ' convidence for Trade')
    if max_val <= 0.50:
        is_on_screen = False

    # if max_val > 0.53:
    #     print("FOUND TemTem Text")
    #     # Show Result.False
    #     # star_width = early_access_image.shape[1]dadaa
    #     # star_height = early_access_image.shape[0]
    #     # top_left = max_loc
    #     # botom_right = (top_left[0] + star_width, top_left[1] + star_height)
    #     # cv.rectangle(game_screen, top_left, botom_right, color=(0,255,255), thickness = 2, lineType = cv.LINE_4)
    #     # cv.imshow('TemTemText?', game_screen)
    # else:
    #     is_on_screen = False
        # print('NOT ON SCREEN..')

    return is_on_screen
    

def take_action():
    global STATE
    global screenshot
    global total_battles
    if STATE == 'Walk':
        on_screen = is_Trade_On_Screen()
        if on_screen:
            walk_line()
        else:
            STATE = 'Battle Started'            
    elif STATE == 'Confirm Battle Started':
        print('Checking if battle started...')
        if not is_Trade_On_Screen:
                STATE = 'Battle Started'
        else:
            STATE = 'Walk'
            print('FALSE ALARM...')
    elif STATE == 'Battle Started':
        while(not is_Temtem_On_Screen()):
            print('Waiting...')
            sleep(1)
        print(STATE)
        sleep(1)
        STATE = 'Detect Luma'
    elif STATE == 'Detect Luma':
        take_screenshot()
        if screenshot is not None:
            found_luma = detect_luma(screenshot)
            print(STATE)
            if found_luma:
                STATE = 'FOUND LUMA'
                send_text()
            else:
                STATE = 'Run Away'
        # else:
        #     print ('SCREENSHOT NONE')
        sleep(2)
    elif STATE == 'Run Away':       
        print(STATE)
        while(is_Temtem_On_Screen()):
            press('8')
            press('8')
            sleep(1/8)
        print('RAN AWAY')
        total_battles += 1
        STATE = 'Walk'
        sleep(2)
        print('Total Encounters: ' + str(total_battles))
    elif STATE == 'FOUND LUMA':
        sleep(30)
        print('Total Encounters: ' + str(total_battles))

def take_screenshot():
    global screenshot
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
    game_hwnd = get_game_window('Temtem')
    # Can't find Window, close program.
    if(not win32gui.IsWindow(game_hwnd) or game_hwnd == 0 or game_hwnd == None):
        cv.destroyAllWindows()
        raise 'Window not found, exiting program.'
    loop_time = time()
    while(True):
        take_action()
        if(STATE != 'Walk'):
            print('Loop took ' + str(time() - loop_time))        
        loop_time = time()
        # Debug to show what the bot sees.
        # cv.imshow('Computer Vision', screenshot)

if __name__ == "__main__":
    main()