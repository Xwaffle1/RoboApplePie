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
from ai import walk_to, origin, position, ai_STATE
from util import *

# Current State of Bot.
STATE = 'Walk'
# Whether the bot detected a luma.
found_luma = False
total_battles = 0
# Width and Height of Screen.
width = 1920
height = 1080

x = 0
y = 0


print('WALKING...')
def take_action():
    global STATE
    global total_battles
    global position, origin, ai_STATE
    if STATE == 'Walk':
        on_screen = is_Trade_On_Screen()
        if on_screen:     
            walk_to(origin[0] + random.randint(1, 5), origin[2] + random.randint(1, 20))
        else:

            for key in ['w', 'a', 's', 'd']:
                gui.keyUp(key)
            STATE = 'Battle Started'            
    elif STATE == 'Battle Started':
        while(not is_Run_On_Screen()):
            print('Waiting...')
            sleep(1)

        STATE = 'Detect Luma'

    elif STATE == 'Detect Luma':
        found_luma = detect_luma()
        print(STATE)
        if found_luma:
            STATE = 'FOUND LUMA'
            # send_text()
        else:
            STATE = 'Fight'    
    elif STATE == 'Fight':       
        print(STATE)
        sleep(1)
        
        press('6')
        sleep(random.randint(300,600)/1000)
        press('1')
        sleep(random.randint(300,600)/1000)
        press('up')
        sleep(random.randint(300,600)/1000)
        press('f')
        sleep(1)
        total_battles += 1
        update_text_file(total_battles)
        STATE = 'Walk'
        while(not is_Trade_On_Screen()):
            sleep(1/8)
            press('f')
        print('Total Encounters: ' + str(total_battles))
    elif STATE == 'FOUND LUMA':
        sleep(30)
        print('Total Encounters: ' + str(total_battles))    

    ai_STATE = ai_STATE

def take_screenshot():
    screenshot = gui.screenshot() 
    screenshot = cv.cvtColor(np.array(screenshot), cv.COLOR_RGB2BGR)
    return screenshot

last_player_pos = time()

def main():

    global width
    global height
    global total_battles
    global last_player_pos
    global origin

    total_battles = read_current_battles()
    print("BOT STARTED WITH: " + str(total_battles) + " battles")

    position = read_player_pos()
    origin = position.copy()

    last_mouse_move = time()
    while(True):
        active_window = gui.getActiveWindow()    
        if active_window != None and active_window.title == 'Temtem':
            if(time() > last_player_pos):
                last_player_pos = time()
                temp = read_player_pos()
                if temp != None:
                    position = temp
            take_action()
            if last_mouse_move + random.randint(10,20) < time():
                last_mouse_move = time()
                if(random.randint(0, 100) < 10):
                    gui.moveTo(width/2 + random.randint(-500,200), random.randint(100,400), duration=(random.randint(1,2) * random.random()))
                    gui.leftClick()

        else:
            print('TemTem not opened..')
            sleep(2)
if __name__ == "__main__":
    main()