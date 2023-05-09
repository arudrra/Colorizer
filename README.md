# Introduction

Colorizer was inspired by recent photography trends where images are often edited with orange and teal tones. 

## Setup

1. Clone the repository.
2. Run `pip install -r requirements.txt` to install the necessary dependencies for Colorizer.

## Colorizer

### How It Works

Colorizer adds strong tones to images by pulling pixels to colors based on the brightness of the pixels. Each pixel falls into one of the following two categories:

1. Shadows (darkest pixels in an image)
2. Highlights (brightest pixels in an image)

Each pixel's brightness is measured on a scale from 0 to 255. Now imagine two contiguous bins corresponding to the two categories:

1. A Shadow Bin containing pixels with a brightness value in between 0 and 89
2. A Highlight Bin containing pixels with a brightness value in between 90 and 255

Colorizer maps the pixels in each bin to a different color. The image on the left is the original image while the images in the middle and right have been edited using colorizer:

![Imgur](https://imgur.com/WVKt0TV.jpg)

The image in the middle has been edited by colorizer using the default setting. All the pixels in the shadow bin have been pulled to teal while the remaining pixels in the highlight bin have pulled to orange. You can recreate the same look using the command `python colorizer.py -f <filepath> -splittone`. The image on the right has also been edited by colorizer but with a different color mapping. The shadows have been mapped to purple (hue value of 280) while the highlights have been mapped to yellow (hue value of 50). You can recreate the same look using the command `python colorizer.py -f <filepath> -splittone -shadowhue 280 -highlighthue 50`.

In bright pictures, most of the pixels will have a high brightness value and fall into the highlight bin. The opposite is true for dark images and the shadow bin. This may result in a dominant tone as shown below:

![Imgur](https://imgur.com/0pG0N1P.jpg)

The image on the left has been edited using the default settings. Since the image is bright, most of the pixels fall into the highlight bin which is mapped to orange. You can change the size of the bins by using the `-shadowthreshold` flag. The flag changes the brightness ranges of the bins. The image on the right was created using the command `python colorizer.py -f <filepath> -splittone -shadowthreshold 160`. By increasing the upper bounds of the shadow bin to 160, more of the image is converted to teal.

You can map the image to three tones instead of two using the `-tritone` flag. Tritoning creates a third bin called the midtone. Each pixel now falls into one of the following three categories:

1. Shadows (darkest pixels in an image)
2. Midtones (pixels between shadows and highlights)
3. Highlights (brightest pixels in an image)

The contiguous bins in tritoning are defined as follows:

1. A Shadow Bin containing pixels with a brightness value in between 0 and 89
2. A Midtone Bin containing pixels with a brightness value in between 90 and 179
3. A Highlight Bin containing pixels with a brightness value in between 180 and 255

### Usage

- `-f` or `--file` specifies the input file to be colorized.

- `-e` or `--extension` specifies the extension to be used for the output file. If not provided, the default string "_colorized" will be appended to the end of the colorized image's filename.

- `-splittone` or `--splittone` specifies whether to apply split-toning to the image. When enabled, the image is split into highlights and shadows, and a different color is applied to each.

- `-tritone` or `--tritone` specifies whether to apply tri-toning to the image. When enabled, the image is split into three bins (shadows, midtones, and highlights), and a different color is applied to each.

- `-shadowthreshold` or `--shadowthreshold` specifies the threshold for shadows in tri-toning. Pixels with a value (brightness) below this threshold are considered shadows. If not provided, the default value of 90 is used.

- `-highlightthreshold` or `--highlightthreshold` specifies the threshold for highlights in tri-toning. Pixels with a value (brightness) above this threshold are considered highlights. If not provided, the default value of 180 is used.

- `-shadowhue` or `--shadowhue` specifies the hue (color) to be used for shadows. The hue is given in degrees, from 0 to 359. If not provided, the default value of 180 (teal) is used.

- `-midtonehue` or `--midtonehue` specifies the hue (color) to be used for midtones in tri-toning. The hue is given in degrees, from 0 to 359. If not provided, the default value of 40 (yellow) is used.

- `-highlighthue` or `--highlighthue` specifies the hue (color) to be used for highlights. The hue is given in degrees, from 0 to 359. If not provided, the default value of 30 (orange) is used.

You must specify a file.

## Palettizer

### How It Works

Coming soon

### Usage

- `-f` or `--file` specifies the input file to be colorized.

- `-g` or `--graph` produces a bar graph, where each bin corresponds to a fixed range of hues, and the height of the bar represents the number of pixels in the image that fall within that range. The color of each bar corresponds to the most frequent hue within that bin.

- `-p` or `--percentage_graph` argument produces a similar bar graph, but the height of each bar represents the percentage of pixels in the image that fall within that bin, rather than the raw pixel count.

- `-s` or `--scale` applies a logarithmic scaling (to the radius axis) to better show the differences between the hue bars. Most of the hues in the graph will not be visible unless the logarithmic scaling is applied.

- `-b` or `--beautify` boosts all percentages to make all colors visible on the graph.

You must specify a file and select either the graph or percentage_graph option.


## Reverse Colorizer

Reverse colorizer changes the colors of a picture to match the colors of another picture.

![Imgur](https://imgur.com/MavVDRS.jpg)

In this example, a color palette is generated from Image 2 and applied to Image 1. The image from which the color palette is generated is called the template image (Image 2 in this example).

### Color Maps

Color maps map hues to other hues. Since cv2 uses 0-180 for the hue range instead of 360, the color map is represented as a dictionary with 180 elements. When the color map is initialized, each hue maps to itself:

```
color_map[1] = 1
color_map[2] = 2
...
color_map[179] = 179
```

For example, imagine an image with a teal sky (hue 90) and a template image with an orange sky (hue 15). Here is how you can map the original image's teal sky to the template's orange sky:

```
color_map[90] = 15
```

Using this color map, reverse colorizer changes any pixel with a hue of 90 (teal) to 15 (orange).

### Bins

Bins are contiguous subarrays of the colormap. Reverse colorizer uses bins to "chunk" color ranges into dominant colors for a palette.

For example, imagine the same image with a teal sky (mostly hue 90) and a template image with an orange sky. The most frequently occuring shade of orange in the template image's sky is hue 15. If the color map only maps the hue 90 to 15, the parts of the sky that are slightly different shades of blue and teal (hue 89 or 91 for example) will remain blue. To solve this issue, colorizer can create a bin for the blue and teal hues from hue 80 to 100 and map all the hues in the bin to orange:

```
color_map[80] = 15
color_map[81] = 15
...
color_map[90] = 15
...
color_map[99] = 15
color_map[100] = 15
```

The bin [80, 100] allows reverse colorizer to recolor the entire blue and teal color range of the sky to a single orange color.

### Significance Value and Threshold

Significance is used to denote how "important" a hue is to an image. The significance value of a hue is computed by dividing the number of times a hue occurs in an image by the number of pixels in the image. The colors in a bin cannot map to a hue with a significance value less than the significance threshold for an image.

To better understand how significance value and threshold are used, here are some examples:

1. If the hue 15 appears 11 times in a 10 pixel by 10 pixel image, the significance value of the hue is 0.11 (11 / 10 * 10).
2. To use colors that make up more than 5% of the template image, set the significance threshold to 0.05.

### Mode-Based Binning

Here is how it works:

1. Divide the color map into contiguous bins of the same size. Perform the following steps for each bin:
2. Find the most frequently occuring hue (referred to as the mode) within the bin.
3. Divide the mode by the number of pixels in the image. This value is referred to as the significance value.
4. If the significance value is greater than or equal to the significance threshold, map all the hues in the bin to the mode.

You must specify the number of bins and the significance threshold. Mode-Based Binning defaults to 6 bins and a significance threshold of 0.05 if the number of bins and/or the significance threshold are not specified. Here is an example of mode-based binning running on a 10 pixel by 10 pixel image with the default settings:

1. The color map is divided into 6 bins with the following hue ranges [0, 29], [30, 59], [60, 89], [90, 119], [120, 149], [150, 179].
2. The hue 10 occurs 20 times and is the most frequently occuring hue for the bin [0, 29].
3. The image has 100 pixels. The significance value for hue 10 is 0.20 (20/100).
4. Since the significance value is greater than the significance threshold, all the hues in the first bin are mapped to the hue 10. Here is how the color map would look:
```
color_map[1] = 10
color_map[2] = 10
...
color_map[29] = 10
```
5. Here is an example of a possible color map after steps 2-4 have been run for each bin:
```
color_map[1] = 10
color_map[2] = 10
...
color_map[29] = 10
color_map[30] = 37
color_map[31] = 37
...
color_map[59] = 37
color_map[60] = 84
color_map[61] = 84
...
color_map[89] = 84
color_map[90] = 103
color_map[91] = 103
...
color_map[119] = 103
color_map[120] = 121
color_map[121] = 121
...
color_map[149] = 121
color_map[150] = 172
color_map[151] = 172
...
color_map[179] = 172
```
Note: This example assumes that each mode was significant. If the hue 172 only appeared 3 times in the previous example, it would have a significance value of 0.03 which is less than the significance threshold of 0.05. In this case, the color map for bin [150, 179] would map each hue to itself since no dominant color was found:
```
color_map[150] = 150
color_map[151] = 151
...
color_map[179] = 179
```

### How Dynamic Binning Works

Much like Mode-Based Binning, Dynamic Binning creates bins for the most frequently occurring colors. However, dynamic bins do not have a fixed bin size or position.

Here is how it works:

1. Calculate the significance value of each hue in an image.
2. Sort the hues by significance in descending order. 
3. Iterate over the hues (from most significant to least significant) and perform step 4 until the user-specified number of bin(s) have been created.
4. If the hue's significance value is greater than the significance threshold and the hue does not fall into an existing bin, create a new bin with range [hue - interval/2, hue + interval/2]. If the new bin overlaps with an existing bin, individually adjust the edges of the new bin until they no longer overlap with the existing bin (thus prioritizing more significant colors and their associated bins). Note: Reverse colorizer accounts for edge cases at 0 and 179 by treating the color map as a circular array.
5. Expand each bin concurrently until the entire color map is filled without any overlap.

### Mode-Based Binning vs Dynamic Binning

Mode-based binning typically provides more subtle color grading with less noise than dynamic binning. Dynamic binning tends to create more drastic and accurate color shifts with fewer bins.

### Troubleshooting Tips

1. If your image has too much noise, increase the number of bins to reduce the harsh hue transitions.
2. If the re-colored image's colors are lacking contrast, increase the `dynamicbininterval` and/or the number of bins for dynamic binning. For mode-based binning, decrease the number of bins.
3. If the threshold warning appears, set the threshold to 0.

### Usage

- `-t` or `--templatefile` specifies the path to the template image file. This is the image that the color palette will be generated from.

- `-f` or `--filetoedit` specifies the path to the image file that will be colorized.

- `-e` or `--extension`: specifies the extension to be used for the output file. If not provided, the default string "_reverse_colorized" will be appended to the end of the colorized image's filename.

- `-b` or `--bins`: specifies the number of primary colors (hues) to "bin" (extract) from an image. If not specified, the default value will be used (6 colors for mode-based color mapping, and 2 colors for dynamically binned color mapping).

- `-s` or `--significance`: specifies the significance threshold, which represents what percentage of an image must be made up of a single color for the color to be considered significant and used. If not specified, the default value will be used (0.05).

- `-m` or `--mode`: specifies whether to use mode-based color mapping or not.

- `-d` or `--dynamic`: specifies whether to use dynamically binned color mapping or not.

- `i` or `--dynamicbininterval`: specifies the starting size of a bin in dynamic binning

You must specify a template file, a file to edit, and select either the mode or dynamic option.