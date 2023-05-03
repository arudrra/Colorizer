#Written by Arudrra Krishnan

import sys
import argparse
from tqdm.auto import trange
from shared_functions import open_and_read_image, save_image
from palettizer import count_all_hues, create_binned_by_mode_color_map, create_dynamically_binned_color_map

#Number of bins represents the number of primary hues to "bin" (extract) from an image
NUM_BINS_FOR_MODE = 6
NUM_BINS_FOR_DYNAMIC = 2
#Significance threshold represents what percentage of an image must be made up of a single color for the color to be considered significant and used
SIGNIFICANCE_THRESHOLD = 0.05
FILE_EXTENSION  = "_reverse_colorized"

#Initialize all settings
def create_and_read_command_line_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--templatefile", type=str)
    parser.add_argument("-f", "--filetoedit", type=str)
    parser.add_argument("-e", "--extension", type=str)
    parser.add_argument("-b", "--bins", type=int)
    parser.add_argument("-s", "--significance", type=float)
    parser.add_argument("-d", "--dynamic", action=argparse.BooleanOptionalAction)
    parser.add_argument("-m", "--mode", action=argparse.BooleanOptionalAction)
    parser.set_defaults(dynamic=False)
    parser.set_defaults(mode=False)
    args = parser.parse_args()
    extension = FILE_EXTENSION if args.extension == None else args.extension
    significance_threshold = SIGNIFICANCE_THRESHOLD if args.significance == None else args.significance
    if args.templatefile == None or args.filetoedit == None:
        print("Usage Error: Please provide both a template file (-t) and a file to edit (-f)")
        sys.exit()
    if args.mode and args.dynamic:
        print("Usage Error: Please select either the dynamic (-d) or mode-based (-m) option")
        sys.exit()
    elif not args.mode and not args.dynamic:
        print("Usage Error: Please select either the dynamic (-d) or mode-based (-m) option")
        sys.exit()
    #1 is by mode, 2 is dynamic, open to adding more algorithms in the future
    reverse_colorizer_mode = 1 if args.mode else 2
    num_bins = args.bins
    if num_bins == None:
        num_bins = NUM_BINS_FOR_MODE if reverse_colorizer_mode == 1 else NUM_BINS_FOR_DYNAMIC
    if args.mode and 180%num_bins != 0:
        print("Usage Error: The number of bins must be a factor of 180 (e.g. 1, 2, 3, 4, 5, 6, 9, 10, 12, 15, 18, 20, 30, 36, 45, 60, 90 or 180)")
        sys.exit()
    if significance_threshold < 0 or significance_threshold > 1:
        print("Usage Error: The significance value must be between 0 and 1 (inclusive)")
        sys.exit()
    return args.templatefile, args.filetoedit, num_bins, significance_threshold, reverse_colorizer_mode, extension

#Applies a color map (hue to hue mapping) to an image
def apply_color_map(color_map, image):
    for row in trange(image.shape[0], ncols = 100, desc ="Progress: ", position=0, leave=True):
        for col in range(image.shape[1]):
            pixel = image[row, col]
            image[row, col] = (color_map[pixel[0]], pixel[1], pixel[2])
    return image

#Recolors image to most frequently occuring colors within a fixed bin size
def bin_tones_by_mode(template_image, image_to_colorize, num_bins, significance_threshold):
    hues = count_all_hues(template_image)
    num_pixels = template_image.shape[0] * template_image.shape[1]
    color_bins, color_map = create_binned_by_mode_color_map(hues, num_pixels, num_bins, significance_threshold)
    image_to_colorize = apply_color_map(color_map, image_to_colorize)
    return image_to_colorize

#Uses dynamic bin sizes and ranges instead of fixed bin sizes
def dynamically_bin_tones(template_image, image_to_colorize, num_bins, significance_threshold):
    hues = count_all_hues(template_image)
    num_pixels = template_image.shape[0] * template_image.shape[1]
    color_bins, color_map = create_dynamically_binned_color_map(hues, num_pixels, num_bins, significance_threshold)
    image_to_colorize = apply_color_map(color_map, image_to_colorize)
    return image_to_colorize

def main():
    #Parse args and extract settings for colorizing
    template_file, file_to_colorize, num_bins, significance_threshold, reverse_colorizer_mode, extension = create_and_read_command_line_arguments()
    #Reverse Colorize Image
    template_image = open_and_read_image(template_file)
    image_to_colorize = open_and_read_image(file_to_colorize)
    if reverse_colorizer_mode == 1:
        image_to_colorize = bin_tones_by_mode(template_image, image_to_colorize, num_bins, significance_threshold)
    else:
        image_to_colorize = dynamically_bin_tones(template_image, image_to_colorize, num_bins, significance_threshold)
    #Save Image
    save_image(image_to_colorize, file_to_colorize, extension)

if __name__=="__main__":
    main()