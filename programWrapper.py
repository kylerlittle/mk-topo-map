
import os as os
import trim as trm
from PIL import Image
from Laplacian_Variance import variance_of_laplacian
import cPickle as pickle
import numpy as np

# Directories
rawImagesDir = "rawImages/"
croppedImagesDir = "croppedImages/"
resizedImagesDir = "resizedImages/"

# Internal Files
internalList = "varLpcMatrixList.pickle"

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
        self.laplacianImageStack = []
        self.numImages = len(os.listdir(rawImagesDir))
        self.3Dmodel = 'not initiated correctly'

    """
    findMaxVarAt: finds maxVariance at a particular 'cluster' (heightDivisor x widthDivisor) of pixels
                  when function is called, it has already been checked that list is non empty
    """
    def __findMaxVarAt__(row, col):
        maxVar = self.laplacianImageStack[0][row][col]
        for laplacianOfIm in self.laplacianImageStack:
            if laplacianOfIm[row][col] > maxVar:
                maxVar = laplacianOfIm[row][col]

    """
    execute: main function to execute all tasks in one (CAREFUL WITH THIS)
    """
    def execute(self, cropThresholdLevel, heightDivisor, widthDivisor):
        self.cropPhotos(cropThresholdLevel)
        self.resizePhotos()
        self.createLaplacianStack(heightDivisor, widthDivisor)

    """
    cropPhotos: crops raw photos to be approximately inline with the outline of the object
    """
    def cropPhotos(self, cropThresholdLevel):
        print "[x] Initiating image cropping"
        imageList = os.listdir(rawImagesDir)
        if not imageList:
            print "Please populate 'rawImages/' with images."
        counter = 1;
        for imStr in imageList:
            trm.trim(rawImagesDir + imStr, croppedImagesDir + "croppedIm" + str(counter) + ".jpg", cropThresholdLevel, counter)
            counter += 1

    """
    resizePhotos: resizes all cropped images to the size of the smallest photo in croppedImagesDir
                  LANCZOS filtering was chosen so as to retain highest downscaling quality
                  performance is least important in this case, so we sacrifice it
    """
    def resizePhotos(self):
        resizeAllImagesTo = smallestImage(croppedImagesDir)        # get smallest image size in directory
        imageList = os.listdir(croppedImagesDir)
        if not imageList:
            print "Try running 'make crop' first."
        else:
            counter = 1   # utilize counter for appropriate file naming
            print "[x] Resizing all images to: ", resizeAllImagesTo
            for imStr in imageList:
                im = Image.open(croppedImagesDir + imStr)
                resizedIm = im.resize(resizeAllImagesTo, resample=Image.LANCZOS)    # resize using LANCZOS filtering
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
            for imStr in imageList:
                varianceMatrix = variance_of_laplacian(resizedImagesDir + imStr, heightDivisor, widthDivisor)
                # For each matrix produced from a single image, append to internal list
                self.laplacianImageStack.append(varianceMatrix)
            with open(internalList, 'wb') as f:
                pickle.dump(self.laplacianImageStack, f, protocol=pickle.HIGHEST_PROTOCOL)

    """
    create3Dmodel: 
    """
    def create3Dmodel(self, startHeight, endHeight):
        if not self.laplacianImageStack:    # i.e. list is empty, populate it
            pickle.load(self.laplacianImageStack)
        if not self.laplacianImageStack:    # if list is still empty, user didn't run createLaplacianStack yet
            print "Try running 'make lpc' first."
        else:
            increment = (endHeight - startHeight) / (self.numImages - 1)
            if (heightLevels > 0):
                heightLevels = np.arange(startHeight, endHeight, increment)
            else:
                heightLevels = np.arange(endHeight, startHeight, increment)
            try:
                assert len(heightLevels) == self.numImages
            except AssertionError:
                print "Array has off-by-one error."
            # Now, simply find max variance at each pixel in the stack.
            # Need to store the height for which this occurs at in self.3D model.
            # This height is heightLevels[laplacianOfIm index].
            self.3Dmodel = laplacianImageStack[0]     # initially each max value is the one in the first matrix
            for laplacianOfIm in self.laplacianImageStack:
                for row in self.laplacianImageStack.length:
                    for col in self.laplacianImageStack.length:
                        maxVar = self.__findMaxVarAt__(row, col)
                        self.3Dmodel[laplacianOfIm
                                                     
            
    """
    o_create3Dmodel: same as create3Dmodel, but breaks once values begin to descend
                     'o' stands for optimized; works because of the physics of optics
    """
    def o_create3Dmodel(self):
        print "Unimplemented."
        
