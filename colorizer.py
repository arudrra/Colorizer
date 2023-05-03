#Written by Arudrra Krishnan

import argparse
import sys
from tqdm.auto import trange
from shared_functions import open_and_read_image, save_image, convert_hsv_to_hex

#Luminosity thresholds for highlights, midtones, and shadows
HIGHLIGHT_THRESHOLD = 180
SHADOW_THRESHOLD = 90

#Hues (default is orange and teal, divided by 2 since cv2's hue range is 0-179)
HIGHLIGHT_HUE = 15
MIDTONE_HUE = 20
SHADOW_HUE = 90

FILE_EXTENSION  = "_colorized"

#Initialize all settings
def initialize_settings():
    #Creating the command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str)
    parser.add_argument("-e", "--extension", type=str)
    #Split tone and tri tone options
    parser.add_argument("-splittone","--splittone", action=argparse.BooleanOptionalAction)
    parser.add_argument("-tritone", "--tritone", action=argparse.BooleanOptionalAction)
    parser.set_defaults(splittone=False)
    parser.set_defaults(tritone=False)
    #Two thresholds (shadows and highlights) are used in tri-toning
    parser.add_argument("-shadowthreshold", "--shadowthreshold", type=int)
    parser.add_argument("-highlightthreshold", "--highlightthreshold", type=int)
    #Three tones (shadows, midtones, highlights)
    parser.add_argument("-shadowhue", "--shadowhue", type=int)
    parser.add_argument("-midtonehue", "--midtonehue", type=int)
    parser.add_argument("-highlighthue", "--highlighthue", type=int)
    #Parse args and extract settings for colorizing
    args = parser.parse_args()
    filepath = args.file
    shadow_threshold = SHADOW_THRESHOLD if args.shadowthreshold == None else args.shadowthreshold
    highlight_threshold = HIGHLIGHT_THRESHOLD if args.highlightthreshold == None else args.highlightthreshold
    highlight_hue = HIGHLIGHT_HUE if args.highlighthue == None else int(args.highlighthue/2) #Divide by 2 to map to cv2's 0-179 hue range
    midtone_hue = MIDTONE_HUE if args.midtonehue == None else int(args.midtonehue/2)
    shadow_hue = SHADOW_HUE if args.shadowhue == None else int(args.shadowhue/2)
    extension = FILE_EXTENSION if args.extension == None else args.extension
    split_tone = args.splittone
    tri_tone = args.tritone
    if args.file == None:
        print("Usage Error: Please provide a file (-f) to edit")
        sys.exit()
    if not split_tone and not tri_tone:
        print("Usage Error: Please select either the split tone (-splittone) or tri tone (-tritone) option")
        sys.exit()
    elif split_tone and tri_tone:
        print("Usage Error: Please select either the split tone (-splittone) or tri tone (-tritone) option")
        sys.exit()
    if shadow_hue < 0 or shadow_hue >= 180 or midtone_hue < 0 or midtone_hue >= 180 or highlight_hue < 0 or highlight_hue >= 180:
        print("Usage Error: Hues must be between 0 and 359 inclusive")
        sys.exit()
    if shadow_threshold > highlight_threshold:
        print("Usage Error: Shadow threshold must be less than highlight threshold")
        sys.exit()
    num_tones = 2 if split_tone else 3
    return filepath, num_tones, shadow_threshold, highlight_threshold, highlight_hue, midtone_hue, shadow_hue, extension

#Split tone pulls an image towards 2 colors
def split_tone(image, threshold, shadow_hue, highlight_hue):
    #Use trange for the progress bar, set the bar color to the highlight hue
    for row in trange(image.shape[0], ncols = 100, desc ="Progress: ", colour=convert_hsv_to_hex(highlight_hue, 255, 255), position=0, leave=True):
        for col in range(image.shape[1]):
            #Get the hue, saturation, and value of each pixel
            pixel = image[row, col]
            value = pixel[2]
            #If the value is less than the threshold, it's a shadow
            if value < threshold:
                image[row,col] = (shadow_hue,pixel[1],pixel[2])
            #Else it's a highlight
            else:
                image[row,col] = (highlight_hue,pixel[1],pixel[2])
    return image

#Tri tone pulls an image towards 3 colors
def tri_tone(image, shadow_threshold, highlight_threshold, shadow_hue, midtone_hue, highlight_hue):
    #Use trange for the progress bar, set the bar color to the highlight hue
    for row in trange(image.shape[0], ncols = 100, desc ="Progress: ", colour=convert_hsv_to_hex(highlight_hue, 255, 255), position=0, leave=True):
        for col in range(image.shape[1]):
            #Get the hue, saturation, and value of each pixel
            pixel = image[row, col]
            value = pixel[2]
            #If the value is less than the shado, it's a shadow
            if value < shadow_threshold:
                image[row,col] = (shadow_hue,pixel[1],pixel[2])
            #Midtones are between
            elif value < highlight_threshold:
                image[row,col] = (midtone_hue,pixel[1],pixel[2])
            #Else it's a highlight
            else:
                image[row,col] = (highlight_hue,pixel[1],pixel[2])
    return image

def main():
    #Parse args and extract settings for colorizing
    filepath, num_tones, shadow_threshold, highlight_threshold, highlight_hue, midtone_hue, shadow_hue, extension = initialize_settings()
    #Open Image
    image = open_and_read_image(filepath)
    #Choose to split tone or tri tone
    if num_tones == 2:
        #The split tone threshold defaults to shadow thresholds
        image = split_tone(image, shadow_threshold, shadow_hue, highlight_hue)
    else:
        image = tri_tone(image, shadow_threshold, highlight_threshold, shadow_hue, midtone_hue, highlight_hue)
    #Save Image
    save_image(image, filepath, extension)

if __name__=="__main__":
    main()