from cv2 import cv2 as cv
import numpy as np
import pyautogui as gui

game_img = cv.imread('assets/no_luma.png', cv.IMREAD_GRAYSCALE)
star_img = cv.imread('assets/star.png', cv.IMREAD_GRAYSCALE)

result = cv.matchTemplate(game_img, star_img, cv.TM_CCOEFF_NORMED )


cv.imshow('Star',result)
cv.waitKey()

if(True):
    raise "DIE"

game2gray = cv.cvtColor(game_img, cv.COLOR_BGR2GRAY)
star2gray = cv.cvtColor(star_img, cv.COLOR_BGR2GRAY)

# cv.imshow('GameImg', game2gray)
# cv.waitKey()

# cv.imshow('Star2Gray', star2gray)
# cv.waitKey()

result = cv.matchTemplate(game2gray, star2gray, cv.TM_CCOEFF_NORMED)

# get best max position
min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

# Show Result.
star_width = star_img.shape[1]
star_height = star_img.shape[0]

top_left = max_loc
botom_right = (top_left[0] + star_width, top_left[1] + star_height)

cv.rectangle(game_img, top_left, botom_right, color=(0,255,255), thickness = 2, lineType = cv.LINE_4)
cv.imshow('Result', game_img)
cv.waitKey()



print('Best Match loc: %s' % str(max_loc))
# print('Best Match confidence: %s'    % str(max_val))

if(max_val > 0.8):
    print("FOUND LUMA")
