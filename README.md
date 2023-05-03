# Introduction

Colorizer was inspired by recent photography trends where images are often edited with orange and teal tones. The image on the left is the original while the image on the right Colorizer.

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

File Options:

```
-f <filepath>
-e <optional extension>
```

Boolean Options:

```
-splittone
-tritone
```

Color Settings:

```
-flag <type [min value, max value]>
```

You can edit the tones and tone distributions using the following settings:

```
-shadowthreshold <int [0:255]>
-highlightthreshold <int [0:255]>
-shadowhue <int [0:359]>
-midtonehue <int [0:359]>
-highlighthue <int [0:359]>
```


Colorizer defaults to and orange and teal 
```
python colorizer.py -f /Pictures/example.jpg --splittone
python colorizer.py -f /Pictures/example.jpg --tritone
```

### Palettizer

Documentation coming soon

### Reverse Colorizer

Documentation coming soon


