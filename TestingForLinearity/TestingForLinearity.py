# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 15:52:00 2017

@author: kylerlittle
"""

#Libraries Included
import numpy as np
import os as os
import sys

# import Laplacian_Variance Function from separate file given a path to it
sys.path.insert(0, '/Users/kylerlittle/Documents/Kuzyk Group Research')
#Laplacian_Variance')
import Laplacian_Variance as lv #import variance_of_laplacian


"""
Function: directory
Description: Given a path & a particular extension of a file, this function
             counts the number of files in that directory with the particular
             extension.
"""
def directory(path,extension):
  list_dir = []   # empty list
  list_dir = os.listdir(path)   # fill list_dir with all files in directory
  count = 0   # count is initially 0
  for file in list_dir:
    if file.endswith(extension):  # file is an image in my case
      count += 1   # add one to the count
  return count


num_images = directory('/Users/kylerlittle/Documents/Kuzyk Group Research/TestingForLinearity', ".JPG")
num_images = float(num_images)   # convert number to double to maintain precision
averageVariance = np.arange(num_images)

file_directory = []
file_directory = os.listdir('/Users/kylerlittle/Documents/Kuzyk Group Research/TestingForLinearity')
print file_directory   # check to make sure I'm looking in the right file
i = 0       # initial index

for file in file_directory:
    if file.endswith(".JPG"):
        varianceArray = lv.variance_of_laplacian(file)
        average = np.average(varianceArray)
        averageVariance[i] = average
        i += 1
print averageVariance


import matplotlib.pyplot as pl

pl.plot(np.arange(num_images), averageVariance)

pl.xlabel("Distance From Table (arb. units)")
pl.ylabel("Average Variance of Laplacian (Measure of Focus)")

pl.show()
