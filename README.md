# Colorizer

Colorizer pulls the brighter areas (highlights) and darker areas (shadows) of an image towards two different user-defined colors. You can use this tool to add user-defined tones to your images.

## Usage

### Specifying Filepath

To run colorizer on one or more pictures, you must specify a folder with supported images. You can specify the filepath for the folder with images by using the `-f` flag as follows:

`python colorize.py -f /Users/arudrra/Images`

Colorizer will then apply the color edits to all supported files in the specified folder (/Users/arudrra/Images in the example above).

Colorizer supports files with JPG, JPEG, and PNG extensions. You can add or remove supported filetypes by modifying the SUPPORTED_EXTENSIONS list in the script. 

### Specifying Filepath
Colorizer requires python3 to work. Depending on your environment, you may have to use python3 instead of python when running colorize:
`python3 colorize.py -f /Users/arudrra/Images`

## Under the Hood

### Editing Base Tones
By default, highlights (brighter parts of the image) are pulled towards orange and shadows (darker parts of the image) are pulled towards teal. You can change the colors that both highlights and shadows are pulled towards with the `-hrgb` (highlight rgb) and `-srgb` (shadow rgb) flags.

`python colorize.py -f /Users/arudrra/Images -srgb 100 141 145 -hrgb 194 0 24`

The `-srgb 100 141 145` flag pulls the shadows towards rgb(100,141,145) and the `-hrgb 194 0 24` flag pulls the highlights towards rgb(194,0,24).

### Computing the Median Luminosity
Colorizer computes the threshold luminosity (brightness) of the image by sampling evenly spaced pixels. The median luminosity of sampled pictures is used as a threshold for pulling colors. Any pixels below with a luminosity lower than the median are classified as shadows while any pixels with a luminosity greater than the median are classified as highlights. Sampling for the median luminosity allows colorizer to classify and pull roughly 50% of the pixels in an image towards one color while pulling the remaining 50% of the pixels towards the other color.

### Adjusting for Distortion
In some images, the color edited image may be distorted due to a bad median value. For example, if most of the image is extremely bright (75% of the pixels are highlights), the median sampling will still force half of the pixels to be pulled towards the shadows (darker tones) so 25% of the highlight pixels will be misclassified as shadows.

You can pass in an adjustment value into the command line via the `-t` flag to compensate for a bad median luminosity. The `-t` flag must be followed by a float value between -1.0 and 1.0 (inclusive). If a `-t` is not passed in, colorizer will assume a `-t` compensation of 0.0 (50% highlights and 50% shadows). A negative `-t` value pulls more than 50% of the image towards the shadow color and the strength of the effect is determined by how close to -1.0 the value is. A positive `-t` value pulls more than 50% of the image towards the highlight color and the strength of the effect is determined by how close to 1.0 the value is.

`python colorize.py -f /Users/arudrra/Images -t .5`


