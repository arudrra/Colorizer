# Colorizer

Colorizer was inspired by recent photography trends where images are often edited with orange and teal tones. Colorizer pulls the brighter areas (highlights) and darker areas (shadows) of an image towards two different colors (orange and teal by default). You can use this tool to add strong tones to your images.

Here is a sample image:

![Imgur](https://i.imgur.com/mieVhD2.jpg)

Here is the same image run through colorizer with the default settings:

![Imgur](https://i.imgur.com/ofig8nj.jpg)

## Usage

### Dependencies

To run colorizer, you will need Python and the Python Imaging Library (PIL).

You can install Python [here](https://www.python.org/downloads/).

To install PIL, you can run the following command:

`pip install Pillow`

If you don't have pip, you can try and install PIL using the instructions [here](https://pillow.readthedocs.io/en/stable/installation.html).

### Specifying Filepath

To run colorizer on one or more pictures, you must specify a folder with supported images. You can specify the filepath for the folder with images by using the `-f` flag as follows:

`python colorize.py -f insert_filepath_here`

If the folder with images is /Users/arudrra/Images, here is how the command should look:

`python colorize.py -f /Users/arudrra/Images`

Colorizer will then apply the color edits to all supported files in the specified folder (/Users/arudrra/Images in the example above). Colorizer saves the file to the same folder with a `_colorized` appended to the end of the filename. You can edit the file ending by changing the `MODIFIED_FILENAME_ADDITION` global in the colorize.py file.

Colorizer supports files with JPG, JPEG, and PNG extensions. You can add or remove supported file types by modifying the `SUPPORTED_EXTENSIONS` global in the script. 

### Python Versions
Colorizer requires python3 to work. Depending on your environment, you may have to use python3 instead of python when running colorize:
`python3 colorize.py -f /Users/arudrra/Images`

### Runtime Notes
Colorizer samples every image and computes every pixel value for each image. This process takes time, especially for larger images. Colorizer tells you which image is being processed at the moment and when the image has been colorized and saved. Quitting the script preemptively will cause the progress for the current image to be canceled.

## Under the Hood

### Editing Base Tones
By default, highlights (brighter parts of the image) are pulled towards orange and shadows (darker parts of the image) are pulled towards teal. You can change the colors that both highlights and shadows are pulled towards with the `-hrgb` (highlight rgb) and `-srgb` (shadow rgb) flags.

`python colorize.py -f /Users/arudrra/Images -srgb 100 141 145 -hrgb 194 0 24`

Here is how the original image would look with the command above. The shadows are pulled towards the blue tone rgb(100,141,145) and highlights are pulled towards the red tone rgb(194,0,24) thus overriding the original orange and teal tones.

![Imgur](https://i.imgur.com/LgxtiET.jpg)

### Computing the Median Luminosity
Colorizer computes the threshold luminosity (brightness) of the image by sampling evenly spaced pixels. The median luminosity of sampled pictures is used as a threshold for pulling colors. Any pixels with a luminosity lower than the median are classified as shadows while any pixels with a luminosity greater than the median are classified as highlights. Sampling for the median luminosity allows colorizer to classify and pull roughly 50% of the pixels in an image towards one color while pulling the remaining 50% of the pixels towards the other color.

### Adjusting for Distortion
In some images, the color edited image may be distorted due to a bad median value. For example, if most of the image is extremely bright (75% of the pixels are highlights), the median sampling will still force half of the pixels to be pulled towards the shadows (darker tones) so 25% of the highlight pixels will be misclassified as shadows.

You can pass in an adjustment value into the command line via the `-t` flag to compensate for a bad median luminosity. The `-t` flag must be followed by a float value between -1.0 and 1.0 (inclusive). If a `-t` is not passed in, colorizer will assume a `-t` compensation of 0.0 (50% highlights and 50% shadows). A negative `-t` value pulls more than 50% of the image towards the shadow color and the strength of the effect is determined by how close to -1.0 the value is. A positive `-t` value pulls more than 50% of the image towards the highlight color and the strength of the effect is determined by how close to 1.0 the value is.

`python colorize.py -f /Users/arudrra/Images -t .5`
