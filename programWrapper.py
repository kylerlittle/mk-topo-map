# Libraries/Modules
import os as os
import trim as trm
from PIL import Image
from Laplacian_Variance import variance_of_laplacian
from threeD_plotting import plot_threeDmodel
from crop_resize_lpc import crop_resize_lpc
import cPickle as pickle
import numpy as np

# Directories
rawImagesDir = "../rawImagesTest1/"
croppedImagesDir = "croppedImages/"
resizedImagesDir = "resizedImages/"

# Internal Files
internalList = "varLpcMatrixList.pickle"
internalThreeDModel = "threeDmodel.npy"

"""
smallestImage: accepts string which refers to a particular directory
               returns 'null' if empty or the size() attribute of the smallest image in the directory
"""
def smallestImage(directory):
    lst = os.listdir(directory)
    try:
        firstImName = lst[0]
    except IndexError:
        print "Empty directory. Cannot find smallest image."
        firstImName = 'null'

    if (firstImName != 'null'):
        currentMin = (100000,100000)        # Any image should be smaller than this... otherwise, I don't want to deal with it
        for imName in lst:
            im = Image.open(directory + imName)
            if (im.size < currentMin):
                currentMin = im.size
            im.close()
    return currentMin


class programWrapper:
    """
    ___init___: constructor
    """
    def __init__(self):
        self.smallestImage = 'invalid'
        self.laplacianImageStack = []
        self.numImages = len(os.listdir(rawImagesDir))
        self.threeDmodel = 'invalid'

    """
    runAll: same as 'execute' but with 'cropPhotos', 'resizePhotos', & 'createLaplacianStack' methods combined
    """
    def runAll(self, middlePercentSaving, cropThresholdLevel, heightDivisor, widthDivisor, startHeight, endHeight, dimension_units):
        crop_resize_lpc(middlePercentSaving, cropThresholdLevel, heightDivisor, widthDivisor)
        self.createThreeDmodel(startHeight, endHeight)
        self.graphModel(dimension_units)
    
    """
    execute: main function to execute all tasks in one (CAREFUL WITH THIS)
             by default, createThreeDmodel is used rather than optimized version
    """
    def execute(self, middlePercentSaving, cropThresholdLevel, heightDivisor, widthDivisor, startHeight, endHeight, dimension_units):
        self.cropPhotos(middlePercentSaving, cropThresholdLevel)
        self.resizePhotos()
        self.createLaplacianStack(heightDivisor, widthDivisor)
        self.createThreeDmodel(startHeight, endHeight)
        self.graphModel(dimension_units)

    """
    cropPhotos: crops 'raw' photos to be approximately inline with the outline of the object
    """
    def cropPhotos(self, middlePercentSaving, cropThresholdLevel):
        imageList = os.listdir(rawImagesDir)
        if not imageList:
            print "Please populate 'rawImages/' with images."
        else:
            print "[x] Initiating image cropping"
            counter = 1;
            for imStr in imageList:
                trm.trim(rawImagesDir + imStr, croppedImagesDir + "croppedIm" + str(counter) + ".jpg", middlePercentSaving, cropThresholdLevel, counter)
                counter += 1

    """
    resizePhotos: resizes all cropped images to the size of the smallest photo in croppedImagesDir
                  LANCZOS filtering was chosen so as to retain highest downscaling quality
                  performance is least important in this case, so we sacrifice it
    """
    def resizePhotos(self):
        self.smallestImage = smallestImage(croppedImagesDir)
        imageList = os.listdir(croppedImagesDir)
        if not imageList:
            print "Try running 'make crop' first."
        else:
            counter = 1   # utilize counter for appropriate file naming
            print "[x] Resizing all images to: ", self.smallestImage
            for imStr in imageList:
                im = Image.open(croppedImagesDir + imStr)
                print "\t[", counter, "] ", im.size[0], ",", im.size[1], "resized to",
                resizedIm = im.resize(self.smallestImage, resample=Image.LANCZOS)    # resize using LANCZOS filtering
                print resizedIm.size[0], ",", resizedIm.size[1]
                resizedIm.save(resizedImagesDir + "readyToAnalyze" + str(counter) + ".jpg")   # save resized im to correct dir
                im.close()
                counter += 1

    """
    createLaplacianStack: for each image in 'resizedImagesDir/', calculate its variance
                          of laplacian matrix; append to internal list; write list to
                          file for further use
    """
    def createLaplacianStack(self, heightDivisor, widthDivisor):
        imageList = os.listdir(resizedImagesDir)
        if not imageList:
            print "Try running 'make resize' first."
        else:
            print "[x] Initiating 'variance_of_laplacian' method on resized images"
            counter = 1   # Counter included for console output
            for imStr in imageList:
                varianceMatrix = variance_of_laplacian(resizedImagesDir + imStr, heightDivisor, widthDivisor, counter)
                counter += 1  
                self.laplacianImageStack.append(varianceMatrix) # For each matrix produced from a single image, append to internal list
            with open(internalList, 'wb') as f:
                pickle.dump(self.laplacianImageStack, f, protocol=pickle.HIGHEST_PROTOCOL)

    """
    __createThreeDmodel__: helper function for createThreeDmodel
    """
    def __createThreeDmodel__(self, startHeight, endHeight):
        heightLevels = np.linspace(0.0, abs(endHeight - startHeight), self.numImages) # by default, linspace includes endpoint
        # Now, simply find max variance at each pixel 'cluster' in the stack.
        self.threeDmodel = np.zeros(self.laplacianImageStack[0].shape)
        print "[x] Creating 3D Model of Size",
        print "(l x w x h): ", self.threeDmodel.shape[0], "x", self.threeDmodel.shape[1], "x", self.numImages
        for index, laplacianOfImMatrix in enumerate(self.laplacianImageStack):
            pointsInFocus = 0
            for row in range(laplacianOfImMatrix.shape[0]):
                for col in range(laplacianOfImMatrix.shape[1]):
                    if laplacianOfImMatrix[row][col] > self.threeDmodel[row][col]:
                        pointsInFocus += 1
                        self.threeDmodel[row][col] = heightLevels[index - 1]   # adjust 'for' loop
            print "\t[", index + 1, "] Percentage of Pixel Clusters Updated: ", pointsInFocus, "/", laplacianOfImMatrix.size, "=",
            print float(pointsInFocus) / laplacianOfImMatrix.size
        # This time, store results using numpy since we're dealing with an array object
        with open(internalThreeDModel, 'wb') as f:
            np.save(f, self.threeDmodel)
            
    """
    createThreeDmodel: endHeight & startHeight are assumed to be nonnegative
                       otherwise, error checking is performed
                       Finds maxVariance at a particular 'cluster' (heightDivisor x widthDivisor) of pixels &
                       stores the height that this occurred at in self.threeDmodel
    """
    def createThreeDmodel(self, startHeight, endHeight):
        try:
            assert isinstance(startHeight, float) == True
            assert isinstance(endHeight, float) == True
        except AssertionError:
            print "One or more of 'startHeight' and 'endHeight' are not floating point values."

        try:
            if os.stat(internalList).st_size > 0:  # checks for empty file; if so, OSError thrown
                with open(internalList, 'rb') as f:
                    try:
                        self.laplacianImageStack = pickle.load(f)
                        self.smallestImage = smallestImage(croppedImagesDir)   # If not running 'execute' style, this needs to be updated
                        self.__createThreeDmodel__(startHeight, endHeight)
                    except IOError:
                        print "Error reading", internalList
        except OSError:
            print "Try running 'make lpc' first."
            
    """
    o_createThreeDmodel: same as createThreeDmodel, but breaks once values begin to descend
                     'o' stands for optimized; works because of the physics of optics
    """
    def o_createThreeDmodel(self):
        print "Unimplemented."

    """
    graphModel: plots the graph produced & displays to screen
    """
    def graphModel(self, dimension_units):
        try:
            if os.stat(internalThreeDModel).st_size > 0:  # checks for empty file; if so, OSError thrown
                with open(internalThreeDModel, 'rb') as f:    # handles open, close, and errors with opening
                    try:   # If file doesn't load correctly, IOError is thrown.
                        self.threeDmodel = np.load(f)
                        plot_threeDmodel(self.threeDmodel, dimension_units)
                    except IOError:
                        print "Error reading", internalThreeDModel
        except OSError:
            print "Try running 'make 3D' first."
