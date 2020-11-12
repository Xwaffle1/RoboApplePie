from util import *
from pyautogui import press
from time import sleep, time
import random

STATE = 'START'
count = 0

sleep(1)

wait = time()
while True:
    if STATE == 'START':
        count = 0
        if is_Fish_Icon_On_Screen():
            print("Starting to Fish...")
            press('F')     
            STATE = 'CATCH'
            sleep(2)

    if STATE == 'CATCH':

        if(time() > wait):
            if(is_Fish_Icon_On_Screen()):
                STATE = 'START'
                continue
            wait = time() + 1

        if is_Fish_On_Screen():
            # sleep(random.randint(10, 20) / 1000)
            press('f')
            count = count + 1
            print('Fish ON...' + str(count))
            sleep(100/1000)
            if(count == 3):
                STATE = 'INSPECT'

    if STATE == 'INSPECT':
        sleep(2)
        while not is_Run_On_Screen():
            sleep(0.25)
            print('Waiting for battle to start.')
            continue
        while is_Run_On_Screen():            
            print('Waiting for manual inspection of fish.')
            sleep(1)
            continue
        STATE = 'START'