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


def trim(inputIm, outputIm, acceptableThreshold, imNum):
    firstArgProvided = True

    try:    
        im = Vips.Image.new_from_file(inputIm)
    except IndexError:
        print "First argument not provided."
        firstArgProvided = False

    if (firstArgProvided):       # Image provided & opened successfully.
        print "\t[", imNum, "] ", im.width, ",", im.height,
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
        print "cropped to", im.width, ",", im.height
        try:
            im.write_to_file(outputIm)
        except IndexError:
            print "Second argument not provided."
    else:
        print "Image to crop not opened successfully."




"""
pre_crop: a method to crop the middle x% of an image in the vertical direction
          i.e. the top/bottom slices are cut off
"""
from PIL import Image


def pre_crop(imStr, croppedImStr, middlePercentSaving, imNum):
    if middlePercentSaving > 1.0 or middlePercentSaving <= 0.0:
        raise ValueError("You must enter a value in the interval (0.0, 1.0].")
    else:
        im = Image.open(imStr)
        imSize = im.size
        print "\t[", imNum, "] ", imSize[0], ",", imSize[1],
        # accepts 4-tuple (left, upper, right, lower)
        upper = int((0.5 - middlePercentSaving/2) * imSize[1]); lower = int((0.5 + middlePercentSaving/2) * imSize[1])
        croppedIm = im.crop((0, upper, imSize[0], lower))
        print "cropped to", imSize[0], ",", imSize[1]
        croppedIm.save(croppedImStr)
