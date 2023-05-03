#Written by Arudrra Krishnan

import cv2
import sys
import numpy as np

#Read image and convert it to the HSV colorspace
def open_and_read_image(filepath):
    try:
        image = cv2.imread(filepath)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        return image
    except Exception as e:
        print(e)
        sys.exit()

#Convert HSV values to hex (default saturation and value to 255 since only hues are manipulated)
def convert_hsv_to_hex(hue, saturation, value):
    color = np.uint8([[[hue, saturation, value]]])
    bgr = tuple(cv2.cvtColor(color,cv2.COLOR_HSV2BGR)[0][0])
    #Convert rgb into hex for display
    red = hex(bgr[2]).split("x")[1]
    green = hex(bgr[1]).split("x")[1]
    blue =  hex(bgr[0]).split("x")[1]
    if len(red) == 1:
        red = "0" + red
    if len(green) == 1:
        green = "0" + green
    if len(blue) == 1:
        blue = "0" + blue
    hex_color = '#' + red + green + blue
    return hex_color

#Convert image back to rgb and save it
def save_image(image, filepath, append_to_end_of_file):
    image = cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
    filepath, extension = filepath.rsplit('.', 1)
    filepath = filepath + append_to_end_of_file + "." + extension
    cv2.imwrite(filepath, image)
    print("Image saved to " + filepath)