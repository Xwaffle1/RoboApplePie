import cv2 as cv
import numpy as np
import os
from time import time
import win32gui 
from PIL import ImageGrab

# Get All Open Windows.
windows_list = []
toplist = []
def enum_win(hwnd, result):
    win_text = win32gui.GetWindowText(hwnd)
    windows_list.append((hwnd, win_text))
win32gui.EnumWindows(enum_win, toplist)
game_hwnd = 0
for (hwnd, win_text) in windows_list:
    if "Photos" in win_text:
        game_hwnd = hwnd


loop_time = time() + 1

while(True):

    # Can't find Window, close program.
    if(not win32gui.IsWindow(game_hwnd)):
        cv.destroyAllWindows()
        print('Window not found, exiting program.')
        break        

    # get an updated image of the game
    position = win32gui.GetWindowRect(game_hwnd)
    can_see_window = win32gui.IsWindowVisible(game_hwnd) and not win32gui.IsIconic(game_hwnd)
    # Take screenshot
    if can_see_window:
        screenshot = ImageGrab.grab(position)
        screenshot = np.array(screenshot)
        screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR)
        cv.imshow('Computer Vision', screenshot)

    # debug the loop rate
    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break