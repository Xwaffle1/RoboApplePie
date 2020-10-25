from cv2 import cv2 as cv
import numpy as np
import pyautogui as gui
import boto3
from PIL import ImageGrab
from win32api import GetSystemMetrics
from time import time

from ai import walk


# game_img = cv.imread('assets/luma_right.png', cv.IMREAD_GRAYSCALE)
# star_img = cv.imread('assets/star_background.png', cv.IMREAD_GRAYSCALE)
# cv.imshow('Star',game_img)
# cv.waitKey()

# cv.imshow('Star',star_img)
# cv.waitKey()

# result = cv.matchTemplate(game_img, star_img, cv.TM_CCOEFF_NORMED)
# min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
# # print('Best Match loc: %s' % str(max_loc))
# print('Best Match confidence: %s'    % str(max_val))


# cv.imshow('Star',result)
# cv.waitKey()


# def gray_scale():
#     game2gray = cv.cvtColor(game_img, cv.COLOR_BGR2GRAY)
#     star2gray = cv.cvtColor(star_img, cv.COLOR_BGR2GRAY)

#     # cv.imshow('GameImg', game2gray)
#     # cv.waitKey()

#     # cv.imshow('Star2Gray', star2gray)
#     # cv.waitKey()

#     result = cv.matchTemplate(star2gray, game2gray, cv.TM_SQDIFF_NORMED)

#     # get best max position
#     min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

#     # Show Result.
#     star_width = star_img.shape[1]
#     star_height = star_img.shape[0]

#     top_left = max_loc
#     botom_right = (top_left[0] + star_width, top_left[1] + star_height)

#     cv.rectangle(game_img, top_left, botom_right, color=(0,255,255), thickness = 2, lineType = cv.LINE_4)
#     cv.imshow('Result', game_img)
#     cv.waitKey()



#     print('Best Match loc: %s' % str(max_loc))wdwdwdwdwdwddddwwwddddddddddddddddwwwwwwdddddddddddddwwwwwwwwdddddddddddddddddddddddwwwwwaaadddsssssssswwwwaaaa
#     # print('Best Match confidence: %s'    % str(max_val))

#     if(max_val > 0.8):
#         print("FOUND LUMA")


def is_Temtem_On_Screen():
    is_on_screen = True
    # game_screen = cv.imread('assets/luma_right.png', cv.IMREAD_GRAYSCALE)
    game_screen = gui.screenshot() 
    game_screen = cv.cvtColor(np.array(game_screen), cv.COLOR_RGB2BGR)
    game_screen = cv.cvtColor(game_screen, cv.COLOR_BGR2GRAY)
    early_access_image = cv.imread('assets/TemTemEarlyAccess.png', cv.IMREAD_GRAYSCALE)
    result = cv.matchTemplate(game_screen, early_access_image, cv.TM_CCOEFF_NORMED)

    # get best max positions
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

    # print('Best Match loc: %s' % str(max_loc))
    print('Best Match confidence: %s'    % str(max_val))
    

    if(max_val > 0.5):
        print("FOUND TemTem Text")
        # Show Result.
        star_width = early_access_image.shape[1]
        star_height = early_access_image.shape[0]
        top_left = max_loc
        botom_right = (top_left[0] + star_width, top_left[1] + star_height)
        cv.rectangle(game_screen, top_left, botom_right, color=(0,255,255), thickness = 2, lineType = cv.LINE_4)
        cv.imshow('TemTemText?', game_screen)
        cv.waitKey()
    else:
        is_on_screen = False

    return is_on_screen

def is_Run_On_Screen():
    is_on_screen = False
    game_screen = specific_screenshot(((width/2)-100 ,(height/2)+300, 200, 200))
    template = cv.imread('assets/run_away.png', cv.IMREAD_GRAYSCALE)
    result = cv.matchTemplate(game_screen, template, cv.TM_CCOEFF_NORMED)

    # get best max positions
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
    
    if(max_val > 0.8):
        is_on_screen = False
        
    return is_on_screen    

def send_text():
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
        Message='A Luma has appeared!',    
    )

    # Print out the response
    print(response)

# # is_Temtem_On_Screen()
# send_text()

def take_screenshot():
    screenshot = gui.screenshot() 
    screenshot = cv.cvtColor(np.array(screenshot), cv.COLOR_RGB2BGR)
    return screenshot

width = 1920
height = 1080
def specific_screenshot(bbox):
    global width
    global height

    screenshot = gui.screenshot(region=bbox) 
    screenshot = cv.cvtColor(np.array(screenshot), cv.COLOR_RGB2BGR)
    screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)

    return screenshot
    # cv.imshow("test", screenshot)
    # cv.waitKey(0)


def is_Trade_On_Screen():
    is_on_screen = False
    game_screen = specific_screenshot((140,(height/2)+50, 200, 200))
    template = cv.imread('assets/Trade.png', cv.IMREAD_GRAYSCALE)
    result = cv.matchTemplate(game_screen, template, cv.TM_CCOEFF_NORMED)
    
    # get best max positions
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
    cv.imshow('test',game_screen)
    cv.waitKey()
    # print(str(max_val) + ' convidence for Trade')
    if max_val >= 0.80:
        is_on_screen = True

    return is_on_screen

def detect_luma():
    found_luma = False
    star_img = cv.imread('assets/star_background.png')
    game2gray = specific_screenshot((width - 800, 0, 800, 200))
    star2gray = cv.cvtColor(star_img, cv.COLOR_BGR2GRAY)

    result = cv.matchTemplate(game2gray, star2gray, cv.TM_CCOEFF_NORMED)

    # get best max positions
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

    # print('Best Match loc: %s' % str(max_loc))
    print('Best Match confidence: %s'    % str(max_val))
    
    cv.imshow('Test', game2gray)
    cv.waitKey()

    if(max_val > 0.7):
        found_luma = True
        print("FOUND LUMA")
            # Show Result.
        # star_width = star_img.shape[1]
        # star_height = star_img.shape[0]

        # top_left = max_loc
        # botom_right = (top_left[0] + star_width, top_left[1] + star_height)

        # cv.rectangle(game_img, top_left, botom_right, color=(0,255,255), thickness = 2, lineType = cv.LINE_4)
    return found_luma    
# while True:
#     take_ac

# temp_time = time()
# detect_luma()
# print(str(time()-temp_time))
