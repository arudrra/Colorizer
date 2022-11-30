from PIL import Image
import argparse
from pathlib import Path
import colorsys
import math

SUPPORTED_EXTENSIONS = ["jpg"]
MODIFIED_FILENAME_ADDITION = "_colorized"
STROKE_WIDTH = 1
LUMINOSITY_R = 0.3
LUMINOSITY_G = 0.59
LUMINOSITY_B = 0.11
MAX_LUMINOSITY = float((LUMINOSITY_R + LUMINOSITY_G + LUMINOSITY_B) * 255)


#You can adjust THRESHOLD, HIGHLIGHT_BOOST, SHADOW_BASE, and HIGHLIGHT_BASE
THRESHOLD = 5
HIGHLIGHT_BOOST = 50
SAMPLING_INTERVAL = 10

#RGB values of base tones that you like
#Shadow (darker) tones will get pulled closer to the shadow base
# SHADOW_BASE = (100,141,145)
# SHADOW_BASE = (0,199,255)
SHADOW_BASE = (0,128,128)

#Highlight (brighter) tones will get pulled closer to the highlight base
# HIGHLIGHT_BASE = (194,0,24)
# HIGHLIGHT_BASE = (255,56,0)
HIGHLIGHT_BASE = (255,140,0)

#DO NOT MODIFY SHADOW_HUE AND HIGHLIGHT_HUE (these are computed using the highlight base and shadow base)
#Extract the Hue from the base tones by coverting the rgb base to hsv
SHADOW_HUE = colorsys.rgb_to_hsv(float(SHADOW_BASE[0])/255.0,float(SHADOW_BASE[1])/255.0,float(SHADOW_BASE[2])/255.0)[0]
HIGHLIGHT_HUE = colorsys.rgb_to_hsv(float(HIGHLIGHT_BASE[0])/255.0,float(HIGHLIGHT_BASE[1])/255.0,float(HIGHLIGHT_BASE[2])/255.0)[0]

#Handle CLI overrides of the base tones
def update_color_settings(new_highlight=None, new_shadow=None, new_threshold=None):
    if new_highlight != None:
        global HIGHLIGHT_BASE
        global HIGHLIGHT_HUE
        HIGHLIGHT_BASE = tuple(new_highlight)
        HIGHLIGHT_HUE = colorsys.rgb_to_hsv(HIGHLIGHT_BASE[0], HIGHLIGHT_BASE[1], HIGHLIGHT_BASE[2])[0]
    if new_shadow != None:
        global SHADOW_BASE
        global SHADOW_HUE
        SHADOW_BASE = tuple(new_shadow)
        SHADOW_HUE = colorsys.rgb_to_hsv(SHADOW_BASE[0],SHADOW_BASE[1],SHADOW_BASE[2])[0]
    if new_threshold != None:
        global THRESHOLD
        THRESHOLD = new_threshold


def get_images(folder):
    path = Path(folder)
    #Add all files with supported extensions to the images list
    files = []
    for extension in SUPPORTED_EXTENSIONS:
        file_objects = path.glob('*.' + extension)
        for file in file_objects:
            files.append(file.resolve())
    return files

#Create custom size borders and stroke for image
def colorize(image_path, file_to_save_as):
    original_image = Image.open(image_path)
    original_image_pixel_map = original_image.load()
    new_image = Image.new(original_image.mode, [original_image.size[0], original_image.size[1]])
    new_image_pixel_map = new_image.load()

    #Sample the threshold at equally spaced points on the image
    #Use the median threshold to detemine highlights (anything higher than the median)
    #and shadows (anything lower than the median)
    thresholds = []
    threshold_row = 0
    threshold_col = 0
    while threshold_row < original_image.size[0]:
        while threshold_col < original_image.size[1]:
            pixel = original_image_pixel_map[threshold_row, threshold_col]
            luminosity = (int)((0.3 * pixel[0]) + (0.59 * pixel[1]) + (0.11 * pixel[2]))
            thresholds.append(luminosity)
            threshold_col += SAMPLING_INTERVAL
        threshold_col = 0
        threshold_row += SAMPLING_INTERVAL
    thresholds.sort()
    THRESHOLD = thresholds[int(len(thresholds)/2)]

    for row in range(original_image.size[0]):
        for col in range(original_image.size[1]):
            pixel = original_image_pixel_map[row, col]
            luminosity = (int)((0.3 * pixel[0]) + (0.59 * pixel[1]) + (0.11 * pixel[2]))
            brightness = (float)((pixel[0] + pixel[1] + pixel[2])/3.0)
            new_pixel = pixel
            # pixel_hsv = colorsys.rgb_to_hsv(pixel[0], pixel[1], pixel[2])
            pixel_hsv = colorsys.rgb_to_hsv(float(pixel[0])/255.0,float(pixel[1])/255.0,float(pixel[2])/255.0)
            if luminosity < THRESHOLD: 
                new_pixel = colorsys.hsv_to_rgb(SHADOW_HUE, pixel_hsv[1], pixel_hsv[2])
            else:
                new_pixel = colorsys.hsv_to_rgb(HIGHLIGHT_HUE, pixel_hsv[1], pixel_hsv[2])
                # new_pixel = colorsys.rgb_to_hsv(HIGHLIGHT_HUE, min(pixel_hsv[1] + HIGHLIGHT_BOOST, 1), min(pixel_hsv[2] + HIGHLIGHT_BOOST, 1))
            new_pixel = ((int)(new_pixel[0] * 255), (int)(new_pixel[1] * 255), (int)(new_pixel[2] * 255))
            new_pixel = (int(math.sqrt(abs(new_pixel[0] - pixel[0]))) + min(new_pixel[0], pixel[0]), int(math.sqrt(abs(new_pixel[1] - pixel[1]))) + min(new_pixel[1], pixel[1]), int(math.sqrt(abs(new_pixel[2] - pixel[2]))) + min(new_pixel[2], pixel[2]))
            # new_pixel = colorsys. colorsys.rgb_to_hsv(float(pixel[0])/255.0,pixel_hsv[1],pixel_hsv[2])
            new_image_pixel_map[row,col] = new_pixel
            #Setting new_image_pixel to the following (luminosity) makes the image black and white instead:
            #new_image_pixel_map[row,col] = (luminosity, luminosity, luminosity)
    original_image.close()
    new_image.save(file_to_save_as)
    new_image.close()

def colorize_all(files):
    for file in files:
        #handles files where there are multiple .'s
        extensions = file.suffixes
        ending = ""
        for extension in extensions:
            ending += extension
        file = str(file)
        file_to_save_as = file[:-len(ending)] + MODIFIED_FILENAME_ADDITION + ending
        colorize(file, file_to_save_as)

def main():
    #Set up arguments for input
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--folder", type=str)
    parser.add_argument("-t", "--threshold", type=float)
    parser.add_argument("-srgb", "--shadow", nargs=3, type=int)
    parser.add_argument("-hrgb", "--highlight", nargs=3, type=int)
    args = parser.parse_args()
    if args.folder != None:
        update_color_settings(args.highlight, args.shadow, args.threshold)
        original_files = get_images(args.folder)
        if len(original_files) != 0:
            colorize_all(original_files)
        else:
            print("Please select a folder with valid files")
    else:
        print("Please provide a folder")


if __name__=="__main__":
    main()

