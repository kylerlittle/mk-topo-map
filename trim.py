#!/usr/bin/env python

"""
The following code was adapted from an implementation on:
https://stackoverflow.com/questions/14211340/automatically-cropping-an-image-with-python-pil
"""

import gi
gi.require_version('Vips', '8.0')       # Ensure the right version is imported
from gi.repository import Vips

# An equivalent of ImageMagick's -trim in pyvip8 ... automatically remove
# "boring" image edges.

# We use .project to sum the rows and columns of a 0/255 mask image, the first
# non-zero row or column is the object edge. We make the mask image with an
# amount-differnt-from-background image plus a threshold.


def trim(inputIm, outputIm, acceptableThreshold):
    firstArgProvided = True

    try:    
        im = Vips.Image.new_from_file(inputIm)
    except IndexError:
        print "First argument not provided."
        firstArgProvided = False

    if (firstArgProvided):       # Image provided & opened successfully.
        # find the value of the pixel at (0, 0) ... we will search for all pixels 
        # significantly different from this
        background = im.getpoint(0, 0)
        
        # we need to smooth the image, subtract the background from every pixel, take 
        # the absolute value of the difference, then threshold
        mask = (im.median(3) - background).abs() > acceptableThreshold
        
        # sum mask rows and columns, then search for the first non-zero sum in each
        # direction
        columns, rows = mask.project()
        
        # .profile() returns a pair (v-profile, h-profile) 
        left = columns.profile()[1].min()
        right = columns.width - columns.flip("horizontal").profile()[1].min()
        top = rows.profile()[0].min()
        bottom = rows.height - rows.flip("vertical").profile()[0].min()
        
        # and now crop the original image
        
        im = im.crop(left, top, right - left, bottom - top)
            
        try:
            im.write_to_file(outputIm)
        except IndexError:
            print "Second argument not provided."
    else:
        print "Image to crop not opened successfully."
