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
# Number of battles currently cached.
total_battles = 0
# Width and Height of Screen.
width = 1920
height = 1080

# Whether the bot should capture the TemTem for you.
catchLuma = False
freeTem = False

SEARCH_FOR = "Occlura"

print('WALKING...')
        
def use_tem_card():
    sleep(random.randint(100,300)/1000)
    press('7')
    sleep(random.randint(100,300)/1000)
    press('e')
    sleep(random.randint(100,300)/1000)
    press('f')

def take_action():
    global STATE, total_battles, catchLuma, position, origin, ai_STATE, SEARCH_FOR
    if STATE == 'Walk':
        on_screen = is_Trade_On_Screen()
        if on_screen:     
            walk_to(origin[0] + random.randint(1, 5), origin[2] + random.randint(-7, -1))
            # if(random.randint(0,2) == 1):
                # walk_circle()
        else:
            for key in ['w', 'a', 's', 'd']:
                gui.keyUp(key)
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
        else:
            if freeTem:
                STATE = 'Free Tem Capture'
            else:
                STATE = 'Run Away'    
    elif STATE == 'Run Away':


        correct_temtem = count_temtem_names(SEARCH_FOR)
        print("FOUND: " + str(correct_temtem))
        
        print(STATE)
        while(is_Run_On_Screen()):
            press('8')
            press('8')
            sleep(1/8)
        print('RAN AWAY')
        total_battles += correct_temtem
        update_text_file(total_battles)
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
    elif STATE == 'Detect FreeTem':
        # detect_free_tem()
        pass
    ai_STATE = STATE

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

        # if(STATE != 'Walk'):
            # print('Loop took ' + str(time() - loop_time))        
        # loop_time = time()

if __name__ == "__main__":
    main()