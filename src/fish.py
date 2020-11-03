from util import *
from pyautogui import press
from time import sleep
import random

STATE = 'START'
count = 0

sleep(1)

while True:
    if STATE == 'START':
        count = 0
        if is_Fish_Icon_On_Screen():
            print("Starting to Fish...")
            press('F')     
            STATE = 'CATCH'
            sleep(2)

    if STATE == 'CATCH':

        if(is_Fish_Icon_On_Screen()):
            STATE = 'START'
            continue

        if is_Fish_On_Screen():
            sleep(random.randint(10, 20) / 1000)
            press('F')
            count = count + 1
            print('Fish ON...' + str(count))
            sleep(100/1000)
            if(count == 3):
                STATE = 'INSPECT'

    if STATE == 'INSPECT':
        sleep(2)
        while not is_Run_On_Screen():
            sleep(0.5)
            print('Waiting for battle to start.')
            continue
        while is_Run_On_Screen():            
            print('Waiting for manual inspection of fish.')
            sleep(1)
            continue
        STATE = 'START'