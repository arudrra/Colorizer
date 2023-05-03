#Written by Arudrra Krishnan

#Imports
from PIL import Image
import argparse
from pathlib import Path
import colorsys

#You can edit the supported extensions or filename addition
SUPPORTED_EXTENSIONS = ["jpg","png","jpeg"]
MODIFIED_FILENAME_ADDITION = "_colorized"

#DO NOT MODIFY, values needed for luminosity computations
LUMINOSITY_R = 0.3
LUMINOSITY_G = 0.59
LUMINOSITY_B = 0.11
MAX_LUMINOSITY = float((LUMINOSITY_R + LUMINOSITY_G + LUMINOSITY_B) * 255)

#You can adjust SAMPLING INTERVAL (smaller values = more sampled points that are closer together)
SAMPLING_INTERVAL = 10

#RGB values of base tones that you like
#Shadow (darker) tones will get pulled closer to the shadow base
SHADOW_BASE = (0,128,128)
#Highlight (brighter) tones will get pulled closer to the highlight base
HIGHLIGHT_BASE = (255,140,0)

#DO NOT MODIFY SHADOW_HUE AND HIGHLIGHT_HUE (these are computed using the highlight base and shadow base)
#Extract the Hue from the base tones by coverting the rgb base to hsv
SHADOW_HUE = colorsys.rgb_to_hsv(float(SHADOW_BASE[0])/255.0,float(SHADOW_BASE[1])/255.0,float(SHADOW_BASE[2])/255.0)[0]
HIGHLIGHT_HUE = colorsys.rgb_to_hsv(float(HIGHLIGHT_BASE[0])/255.0,float(HIGHLIGHT_BASE[1])/255.0,float(HIGHLIGHT_BASE[2])/255.0)[0]

#DO NOT MODIFY THRESHOLD IN SCRIPT, instead modify THRESHOLD through the the command line arguments by using '-t'
THRESHOLD = 0.0


#Handle CLI overrides of the base tones and threshold
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
    if new_threshold != None and new_threshold >= -1 and new_threshold <= 1:
        global THRESHOLD
        #Flip threshold to be more intuitive for users (was inverted before)
        #more highlights = positive number between 0.0 and 1.0
        #more shadows = negative number between -1.0 and 0.0
        THRESHOLD = -new_threshold

#Get all images with supported extensions in the given folder
def get_images(folder):
    path = Path(folder)
    #Add all files with supported extensions to the images list
    files = []
    for extension in SUPPORTED_EXTENSIONS:
        file_objects = path.glob('*.' + extension)
        for file in file_objects:
            files.append(file.resolve())
    return files

#Applies color edit to an image and saves it
def colorize(image_path, file_to_save_as):
    #Opening and setting up the images
    original_image = Image.open(image_path)
    original_image_pixel_map = original_image.load()
    new_image = Image.new(original_image.mode, [original_image.size[0], original_image.size[1]])
    new_image_pixel_map = new_image.load()

    #Sample the average "brightness" at equally spaced (defined by sampling interval) points on the image
    thresholds = []
    threshold_row = 0
    threshold_col = 0
    #Loop through all the pixels
    while threshold_row < original_image.size[0]:
        while threshold_col < original_image.size[1]:
            pixel = original_image_pixel_map[threshold_row, threshold_col]
            luminosity = (int)((LUMINOSITY_R * pixel[0]) + (LUMINOSITY_G * pixel[1]) + (LUMINOSITY_B * pixel[2]))
            thresholds.append(luminosity)
            threshold_col += SAMPLING_INTERVAL
        threshold_col = 0
        threshold_row += SAMPLING_INTERVAL
    #Select the median "brightness" to set as the threshold
    thresholds.sort()
    balanced_threshold = thresholds[int(len(thresholds)/2)]
    #Adjust threshold based on user input (pull the threshold up or down by a percentage)
    #Example: If THRESHOLD = 0.5, the brightness threshold will be lowered so 75% of the image using the base settings will be highlights (orange)
    #Default is 0 pull so roughly half of the image should be highlights (orange by default) and the other half should be shadows (teal by default)
    balanced_threshold += balanced_threshold * THRESHOLD
    #Loop through all the pixels
    for row in range(original_image.size[0]):
        for col in range(original_image.size[1]):
            pixel = original_image_pixel_map[row, col]
            #Measure the luminosity or "brightness" of the pixel
            luminosity = (int)((LUMINOSITY_R * pixel[0]) + (LUMINOSITY_G * pixel[1]) + (LUMINOSITY_B * pixel[2]))
            new_pixel = pixel
            #Convert pixel from RGB representation to HSV
            pixel_hsv = colorsys.rgb_to_hsv(float(pixel[0])/255.0,float(pixel[1])/255.0,float(pixel[2])/255.0)
            #Use the user adjusted luminosity to detemine highlights (anything higher than the threshold) and shadows (anything lower than the threshold)
            #Change the hue to highlight hue or shadow hue but retain the saturation and value to preserve the original image
            if luminosity < balanced_threshold: 
                new_pixel = colorsys.hsv_to_rgb(SHADOW_HUE, pixel_hsv[1], pixel_hsv[2])
            else:
                new_pixel = colorsys.hsv_to_rgb(HIGHLIGHT_HUE, pixel_hsv[1], pixel_hsv[2])
            #Convert the new pixel to RGB
            new_pixel = ((int)(new_pixel[0] * 255), (int)(new_pixel[1] * 255), (int)(new_pixel[2] * 255))
            new_image_pixel_map[row,col] = new_pixel
            #Setting new_image_pixel to the following (luminosity) makes the image black and white instead:
            #new_image_pixel_map[row,col] = (luminosity, luminosity, luminosity)

    #Close and save
    original_image.close()
    new_image.save(file_to_save_as)
    new_image.close()

#Calls color edit function on each file (in addition to creating the file save path)
def colorize_all(files):
    for file in files:
        print("Colorizing File " + str(file))
        #handles files where there are multiple .'s
        extensions = file.suffixes
        ending = ""
        for extension in extensions:
            ending += extension
        file = str(file)
        #Create the file save name
        file_to_save_as = file[:-len(ending)] + MODIFIED_FILENAME_ADDITION + ending
        #edit the colors and save the file to the new filepath
        colorize(file, file_to_save_as)
        print("File saved to " + file_to_save_as)

def main():
    #Set up arguments for input
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--folder", type=str)
    parser.add_argument("-t", "--threshold", type=float)
    parser.add_argument("-srgb", "--shadow", nargs=3, type=int)
    parser.add_argument("-hrgb", "--highlight", nargs=3, type=int)
    args = parser.parse_args()
    #Check for bad user input (no folder)
    if args.folder != None:
        update_color_settings(args.highlight, args.shadow, args.threshold)
        original_files = get_images(args.folder)
        #Check for empty folder
        if len(original_files) != 0:
            #Main functions run here
            colorize_all(original_files)
        else:
            print("Please provide a folder with valid files")
    else:
        print("Please provide a folder")

if __name__=="__main__":
    main()
