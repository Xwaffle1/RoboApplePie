from cv2 import cv2 as cv
import pytesseract
from util import specific_screenshot_color, detect_luma, count_temtem_names
from time import time, sleep
import numpy as np

width = 1920
height = 1080