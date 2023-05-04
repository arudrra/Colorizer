# Introduction

Colorizer was inspired by recent photography trends where images are often edited with orange and teal tones. The image on the left is the original while the image on the right has been edited using Colorizer.

![Imgur](https://imgur.com/yyRh52s.jpg)

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

You must specify a file and select either the graph or percentage_graph options.


## Reverse Colorizer

### How It Works

Coming soon

### Usage

- `-t` or `--templatefile` specifies the path to the template image file. This is the image that the color palette will be generated from.

- `-f` or `--filetoedit` specifies the path to the image file that will be colorized.

- `-e` or `--extension`: specifies the extension to be used for the output file. If not provided, the default string "_colorized" will be appended to the end of the colorized image's filename.

- `-b` or `--bins`: specifies the number of primary colors (hues) to "bin" (extract) from an image. If not specified, the default value will be used (6 colors for mode-based color mapping, and 2 colors for dynamically binned color mapping).

- `-s` or `--significance`: specifies the significance threshold, which represents what percentage of an image must be made up of a single color for the color to be considered significant and used. If not specified, the default value will be used (0.05).

- `-d` or `--dynamic`: specifies whether to use dynamically binned color mapping or not. If not specified, mode-based color mapping will be used.

- `-m` or `--mode`: specifies whether to use mode-based color mapping or not. If not specified, dynamically binned color mapping will be used.



