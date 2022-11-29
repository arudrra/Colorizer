# Colorizer

## Introduction
Colorizer pulls the brighter areas (highlights) and darker areas (shadows) of an image towards two different user-defined colors. You can use this tool to add user-defined tones to your images.

## Usage

### Editing Variables
If you want to change the tones and strength of the effect, you can change any of the following variables
1. HIGHLIGHT_BASE
2. SHADOW_BASE
3. THRESHOLD

## Under the Hood
Colorizer leverages RGB and HSV values to "pull" the pixels in the image towards complimentary colors. Here's how it works:


