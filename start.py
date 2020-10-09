import cv2 as cv
import numpy as np
import os
import copy
from time import time
import win32gui 
from PIL import ImageGrab
import pyautogui as gui
from pyautogui import press, typewrite, hotkey

# Current State of Bot.
STATE = 'Walk'
# Most Recent Screenshot taken.
screenshot = None 
# Whether the bot detected a luma.
found_luma = False

def detect_luma(game_img):
    found_luma = False
    star_img = cv.imread('star_background.png')

    game2gray = cv.cvtColor(game_img, cv.COLOR_BGR2GRAY)
    star2gray = cv.cvtColor(star_img, cv.COLOR_BGR2GRAY)

    result = cv.matchTemplate(game2gray, star2gray, cv.TM_CCOEFF_NORMED)

    # get best max position
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

def take_action(state):
    if state == 'Walk':
        print(state)
    elif state == 'Battle Started'
        print(state)
    elif state == 'Detect Luma'
        # Use Copy of ScreenShot because our loop changes screenshot so fast.
        screenshot_copy = copy(screenshot)
        found_luma = detect_luma(screenshot_copy)
        print(state)
    elif state == 'Run Away'
        print(state)


def main():
    game_hwnd = get_game_window('Spotify Premium')
    loop_time = time() + 1
    while(True):
        # Can't find Window, close program.
        if(not win32gui.IsWindow(game_hwnd)):
            cv.destroyAllWindows()
            print('Window not found, exiting program.')
            break        

        # get an updated image of the game
        # position = win32gui.GetWindowRect(game_hwnd)
        # can_see_window = win32gui.IsWindowVisible(game_hwnd) and not win32gui.IsIconic(game_hwnd)
        # # Take screenshot
        # if can_see_window:
        #     screenshot = ImageGrab.grab(position)
        #     screenshot = np.array(screenshot)
        #     screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR)
        #     cv.imshow('Computer Vision', screenshot)

        # Screenshot of WHOLE monitor.
        screenshot = gui.screenshot() 
        screenshot = cv.cvtColor(np.array(screenshot), cv.COLOR_RGB2BGR)

        take_action(STATE)        

        # Debug to show what the bot sees.
        cv.imshow('Computer Vision', screenshot)

        # debug the loop rate
        print('FPS {}'.format(1 / (time() - loop_time)))
        loop_time = time()    

        # press 'q' with the output window focused to exit.
        # waits 1 ms every loop to process key presses
        if cv.waitKey(1) == ord('q') or found_luma:
            cv.destroyAllWindows()
            break

