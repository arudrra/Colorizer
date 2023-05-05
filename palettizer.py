#Written by Arudrra Krishnan

import sys
import argparse
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from shared_functions import open_and_read_image, convert_hsv_to_hex

BEAUTIFY_BOOST = 7

#Initialize all settings
def initialize_settings():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str)
    parser.add_argument("-g", "--graph", action=argparse.BooleanOptionalAction)
    parser.add_argument("-p", "--percentagegraph", action=argparse.BooleanOptionalAction)
    parser.add_argument("-s", "--scale", action=argparse.BooleanOptionalAction)
    parser.add_argument("-b", "--beautify", action=argparse.BooleanOptionalAction)
    parser.set_defaults(graph=False)
    parser.set_defaults(percentagegraph=False)
    parser.set_defaults(scale=False)
    parser.set_defaults(scale=False)
    args = parser.parse_args()
    if args.graph and args.percentagegraph:
        print("Usage Error: Please select either the graph (-g) or percentage graph (-p) option")
        sys.exit()
    elif not args.graph and not args.percentagegraph:
        print("Usage Error: Please select either the graph (-g) or percentage graph (-p) option")
        sys.exit()
    graph_option = 1 if args.graph else 2
    if args.beautify and graph_option == 1:
        print("Beautify is only available for percentage graphs")
        sys.exit()
    if args.scale and args.beautify:
        print("Scale and beautify both improve legibility. When used together, they can create wildly innacurate graphs. Please select either scale or beautify.")
        sys.exit()
    return args.file, graph_option, args.scale, args.beautify

#Counts the number of occurrences of each hue
def count_all_hues(image):
    #CV2's colorspace uses 0-180 for the hue range instead of 360
    hues = [0 for i in range(180)]
    for row in range(image.shape[0]):
        for col in range(image.shape[1]):
            #Get the hue, saturation, and value of each pixel
            hue = image[row, col][0]
            #Hue value is represented by the index in the array multiplied by 2
            hues[hue] += 1
    return hues

#Create color bins for the most frequently occuring colors within a fixed bin size
def create_binned_by_mode_color_map(hues, num_pixels, num_bins, significance_threshold):
    #Color Interval is the hue range for each bin (e.g. 180 hues / 6 bins = 30 hues per bin)
    color_interval = int(180/num_bins)
    color_bins = dict()
    color_map = dict()
    for hue in range(180):
        color_map[hue] = hue
    #Select the most frequent hue for each bin
    #For example if hue 10 is the most frequently occuring hue for the bin representing hues 1-30
    #All hues in the bin (hues 1-30) would map to hue 10
    for base in range(int(180/color_interval)):
        most_frequent_hue = -1
        occurances = 0
        for hue in range(base * color_interval, (base * color_interval + color_interval)):
            if occurances < hues[hue]:
                most_frequent_hue = hue
                occurances = hues[hue]
        #If the most frequent color occurs enough to be considered significant, map all the colors in the bin to the mode
        if float(occurances/num_pixels) > significance_threshold:
            color_bins[most_frequent_hue] = occurances
            for hue in range(base * color_interval,(base * color_interval + color_interval)):
                color_map[hue] = most_frequent_hue
    return color_bins, color_map

#Expand each bin concurrently until the entire color map is filled without any overlap
def calculate_and_populate_color_map_interval(color_map, hue, interval):
    interval = int(interval/2)
    #Calculate the color interval for the bin (accounting for the circular array ending at 179)
    bin_interval_end = (hue + interval) % 180
    bin_interval_start = hue - interval
    if hue - interval < 0:
        bin_interval_start = 180 + bin_interval_start
    #Format for the interval is (start of bin, end of bin, bin hue)
    bin_interval = (bin_interval_start, bin_interval_end)
    #Set all colors within the color interval to the most frequently occuring hue, account for the circular array
    color_map[hue] = hue
    for i in range(hue + 1, hue + interval + 1):
        color_map[i%180] = hue        
    for i in range(hue - interval, hue):
        if i >= 0:
            color_map[i] = hue
        else:
            color_map[180+i] = hue
    #Since the colormap is passed by reference, only return the computed bin interval
    return bin_interval

#Expands the color bins until they cover the entire color map
def basic_merge_intervals(color_map, intervals):
    intervals = [[interval[0], interval[1], interval[2]] for interval in intervals]
    num_intervals = len(intervals)
    interval_expanding = True
    while interval_expanding:
        interval_expanding = False
        for i in range(num_intervals):
            new_upper_bound = (intervals[i][1]+1)%180
            new_lower_bound = intervals[i][0] - 1
            hue = intervals[i][2]
            if new_lower_bound < 0:
                new_lower_bound = 179
            if color_map[new_upper_bound] == -1:
                color_map[new_upper_bound] = hue
                intervals[i][1] = new_upper_bound
                interval_expanding = True
            if color_map[new_lower_bound] == -1:
                color_map[new_lower_bound] = hue
                intervals[i][0] = new_lower_bound
                interval_expanding = True
    return intervals

#Create color bins for the most frequently occuring colors
def create_dynamically_binned_color_map(hues, num_pixels, num_bins, significance_threshold, dynamic_bin_interval):
    #Created a list (sorted by number of occurences of each hue)
    hues_sorted_by_occurences = []
    for i in range(180):
        hues_sorted_by_occurences.append((hues[i]/num_pixels, i))
    hues_sorted_by_occurences = sorted(hues_sorted_by_occurences)
    hues_sorted_by_occurences = hues_sorted_by_occurences[::-1]
    #Initialize color map, use -1 to check if the mapping for a hue has not been set
    color_map = dict()
    for hue in range(180):
        color_map[hue] = -1
    color_bins = dict()
    #Dynamically create bins
    bins = 0
    bin_intervals = []
    for i in range(180):
        significance, hue = hues_sorted_by_occurences[i][0], hues_sorted_by_occurences[i][1]
        if significance < significance_threshold:
            print("Only " + str(bins) + " significant colors were found. Please lower the threshold for more color bins.")
            break
        if color_map[hue] == -1:
            bin_interval = calculate_and_populate_color_map_interval(color_map, hue, dynamic_bin_interval)
            bin_interval = (bin_interval[0], bin_interval[1], hue, significance)
            bin_intervals.append(bin_interval)
            bins += 1
            if bins == num_bins:
                break
    #The color map only 
    bin_intervals = basic_merge_intervals(color_map, bin_intervals)
    #Will add a softener function here in the future to make the transition between color intervals less harsh
    return color_bins, color_map

#Functions that create or help create graphs/visualizations

#Creates and converts (from hsv to rgb) all the colors for the graph
def create_colors_for_graph(hues):
    graph_colors = []
    for hue in hues:
        #Convert each hue into rgb (fix saturation and value at 255)
        hex_color = convert_hsv_to_hex(hue, 255, 255)
        graph_colors.append(hex_color)
    return graph_colors

#Create a list of 180 colors for the polar graph color wheel
def create_full_spectrum_of_colors_for_graph():
    #The color range is the full hue wheel (represented as 0 to 180 instead of 360 in cv2)
    color_range = [i for i in range(180)]
    #Creating the colors for the graph (hsv to rgb conversion)
    graph_colors = create_colors_for_graph(color_range)
    return graph_colors

#Helper function that calculates some default settings for an image
def calculate_width_and_theta_for_polar_bar_graph(num_bars):
    width = 2 * np.pi / num_bars
    theta = [(i+1) * width for i in range(num_bars)]
    return width, theta

#Sets up and displays graph
def create_and_display_graph(data, graph_colors, graph_title, scale=False, bar_outline_color="white"):
    mpl.rcParams['toolbar'] = 'None'
    plt.figure(figsize=(20,10), num=graph_title)
    ax = plt.subplot(111, polar=True)
    width, theta = calculate_width_and_theta_for_polar_bar_graph(len(data))
    ax.bar(x=theta, height=data, width=width, linewidth=2, color=graph_colors, edgecolor=bar_outline_color)
    if scale:
        ax.set_rscale("symlog")
    plt.show()

#Counts the number of occurrences of each hue for shadows and highlights (separately)
#No current use case at the moment, not accessible through the CLI
def create_hue_value_pair_graph(image):
    graph_colors = create_full_spectrum_of_colors_for_graph()
    interval, theta = calculate_width_and_theta_for_polar_bar_graph(180)
    hues = []
    values = []
    colors = []
    for row in range(image.shape[0]):
        for col in range(image.shape[1]):
            #Get the hue, saturation, and value of each pixel
            hue, saturation, value = image[row, col]
            hues.append(theta[hue])
            values.append(value)
            colors.append(graph_colors[hue])
    fig = plt.figure()
    ax = fig.add_subplot(projection='polar')
    ax.scatter(hues, values, color=colors, s=1)
    plt.show()

#Functions to create polar bar graphs
def measure_occurrences_of_all_hues(image, scale):
    hues = count_all_hues(image)
    graph_colors = create_full_spectrum_of_colors_for_graph()
    bar_outline_color = "white"
    if not scale:
        print("This graph is not scaled (only the most frequently occuring colors will be visible). To better visualize all the colors in the graph use the -s flag.")
        bar_outline_color = None
    create_and_display_graph(hues, graph_colors, "Occurences of All Hues", scale, bar_outline_color)

def measure_percentage_of_hue_occurrences(image, scale, beautify):
    hues = count_all_hues(image)
    graph_colors = create_full_spectrum_of_colors_for_graph()
    num_pixels = image.shape[0] * image.shape[1]
    for i in range(180):
        hues[i] = float(hues[i]/num_pixels)*100
    #Boosts all percentages to make all colors visible on the graph
    bar_outline_color = "None"
    if beautify:
        for i in range(180):
            hues[i] += BEAUTIFY_BOOST
        print("All percentages in the graph have been increased by " + str(BEAUTIFY_BOOST) +"%")
        bar_outline_color = 'white'
    else:
        print("This graph has not been boosted with beautify (only the most frequently occuring colors will appear). To better visualize all the colors in the graph use the -b flag.")
    create_and_display_graph(hues, graph_colors, "Percentage of All Hues", scale, bar_outline_color)

#Displays results from reverse_colorizer binning
#Not accessible through the CLI
#Usage: measure_binned_occurrences(image, 12, 0)
def measure_binned_occurrences(image, num_bins, significance_threshold):
    hues = count_all_hues(image)
    num_pixels = image.shape[0] * image.shape[1]
    color_bins, color_map = create_binned_by_mode_color_map(hues, num_pixels, num_bins, significance_threshold)
    binned_hues = []
    binned_hues_occurrences = []
    for hue in color_bins:
        binned_hues.append(hue)
        binned_hues_occurrences.append(color_bins[hue])
    graph_colors = create_colors_for_graph(binned_hues)
    create_and_display_graph(binned_hues_occurrences, graph_colors, "Binned by Mode Hues")

def main():
    #Parse args and extract settings for analysis
    filepath, graph_option, scale, beautify = initialize_settings()
    image = open_and_read_image(filepath)
    if graph_option == 1:
        measure_occurrences_of_all_hues(image, scale)
    else:
        measure_percentage_of_hue_occurrences(image, scale, beautify)

if __name__=="__main__":
    main()