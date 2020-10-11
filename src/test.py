from cv2 import cv2 as cv
import numpy as np
import pyautogui as gui



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



#     print('Best Match loc: %s' % str(max_loc))
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

is_Temtem_On_Screen()
