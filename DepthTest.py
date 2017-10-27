# -*- coding: utf-8 -*-
"""
Created on Tue May  9 13:30:32 2017

@author: kylerlittle
"""

import numpy as np
import os as os
import sys

# import "directory" function from separate file given a path to it
sys.path.insert(0, '/Users/kylerlittle/Documents/Kuzyk Group Research/TestingForLinearity')
from TestingForLinearity import directory

# import Laplacian_Variance Function from separate file given a path to it
sys.path.insert(0, '/Users/kylerlittle/Documents/Kuzyk Group Research')
import Laplacian_Variance as lv                 #import variance_of_laplacian

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
 ___________________________________________________
| Object 3D Reconstruction from series of 2D Images |
 ---------------------------------------------------

Description: From a series of 2D images above an object, taken at equally
             spaced distance intervals, this program will recover the
             depth of the object to scale. To recover the correct x-y 
             dimensions, it is straightforward. The CCD array's physical
             dimensions must be measured and corresponded with the
             pixelation of its images (recall that the pixel's dimensions
             must be divided by 10 since Laplacian_Variance does such).
             This will be done in a separate file which plots the object.

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# 1. Determine the number of images to analyze.
numImages = directory('/Users/kylerlittle/Documents/Kuzyk Group Research/DepthTest1', ".JPG")
numImages = float(numImages)

# 2. Determine spacing between images taken. This will be the distance the 
#    Arduino incrementally moves the translational stage at. 
VerticalImageSeparationDistance = 0.02          # in centimeters
HeightChangeArray = np.arange(0, numImages, VerticalImageSeparationDistance)

# 3. Create a matrix, whose coordinates will represent a 3-D construction
#    of the image, once it is analyzed. The x-y coordinate will represent any
#    xy coordinate in the image itself, while its entry will represent the
#    z coordinate.
imageHeight = 0
imageWidth = 0
threeDconstruction = np.zeros(imageHeight,imageWidth)
varianceValues = np.zeros(imageHeight,imageWidth)

# 4. Go through all images in the order that they are taken. Correspond
#    each xy position that is IN FOCUS with a height in the z plane
#    that the portion of the image is at. There will be no 'absolute'
#    height measure. Height measurements are with respect to a change in
#    height. Ultimately, this will result in all fiber corrogations being
#    mapped to a specific xy location. What I will need to do to completely
#    recovery the image's dimensions is insert two 'scale' bars from
#    actual measurements for the x-y axes. Then, the image will be
#    fully recontructed as a 3D model!
file_directory = []
file_directory = os.listdir('/Users/kylerlittle/Documents/Kuzyk Group Research/DepthTest1')

# The order that the 'for' loop runs through each image will match the order
# of the HeightChangeArray.
for file in file_directory:
    if file.endswith(".JPG"):
        varianceArray = lv.variance_of_laplacian(file)

        # Find maximum variance value in varianceArray
        maxValue = varianceArray[0]     # initially, max is first entry
        for entry in varianceArray:
            if entry > maxValue:
                maxValue = entry
                
        # Find all values within 2% of the maximum. These are likely in focus.
        # I might need to adjust this figure.
        thresholdValue = 0.98 * maxValue        # indicating IN FOCUS
        for index, entry in enumerate(varianceArray):
            if entry > thresholdValue and varianceValues[index] < entry:
                # Part 1 of conditional: if entry is above threshold 
                # Part 2 of conditional: if varianceValues[index] is zero or
                # a nonempty position is being overriden, this ensures that
                # we choose the value with a higher variance associated with it
                varianceValues[index] = entry
                threeDconstruction[index] = HeightChangeArray[index]
                    
            