# Libraries/Modules
import os as os
import trim as trm
from PIL import Image
from Laplacian_Variance import variance_of_laplacian
from threeD_plotting import plot_threeDmodel
import cPickle as pickle
import numpy as np

# Directories
rawImagesDir = "testImages/"
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
        self.laplacianImageStack = []
        self.numImages = len(os.listdir(rawImagesDir))
        self.threeDmodel = np.zeros((327,87))

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
             by default, createThreeDmodel is used rather than optimized version
    """
    def execute(self, cropThresholdLevel, heightDivisor, widthDivisor, startHeight, endHeight):
        self.cropPhotos(cropThresholdLevel)
        self.resizePhotos()
        self.createLaplacianStack(heightDivisor, widthDivisor)
        self.createThreeDmodel(startHeight, endHeight)
        self.graphModel()

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
        if not self.laplacianImageStack:    # i.e. list is empty, populate it
            with open(internalList, 'rb') as f:
                self.laplacianImageStack = pickle.load(f)
        if not self.laplacianImageStack:    # if list is still empty, user didn't run createLaplacianStack yet
            print "Try running 'make lpc' first."
        else:
            heightLevels = np.linspace(0.0, abs(endHeight - startHeight), self.numImages) # by default, linspace includes endpoint
            # Now, simply find max variance at each pixel 'cluster' in the stack.
            self.threeDmodel = np.zeros(self.laplacianImageStack[0].shape)   # initialize w/ correct size
            print "3D Model Dimensions (l x w x h): ", self.threeDmodel.shape[0], "x", self.threeDmodel.shape[1], "x", self.numImages
            for index, laplacianOfImMatrix in enumerate(self.laplacianImageStack):
                for row in range(laplacianOfImMatrix.shape[0]):
                    for col in range(laplacianOfImMatrix.shape[1]):
                        if laplacianOfImMatrix[row][col] > self.threeDmodel[row][col]:
                            self.threeDmodel[row][col] = heightLevels[index - 1]   # adjust 'for' loop
            # This time, store results using numpy since we're dealing with an array object
            with open(internalThreeDModel, 'wb') as f:
                np.save(f, self.threeDmodel)
            
    """
    o_createThreeDmodel: same as createThreeDmodel, but breaks once values begin to descend
                     'o' stands for optimized; works because of the physics of optics
    """
    def o_createThreeDmodel(self):
        print "Unimplemented."

    """
    graphModel: plots the graph produced & displays to screen
    """
    def graphModel(self):
        if not self.threeDmodel.size:    # i.e. array is empty, populate it
            with open(internalThreeDModel, 'rb') as f:
                self.threeDmodel = np.load(f)
        if not self.threeDmodel.size:    # if threeDmodel is still empty, user didn't run createThreeDmodel yet
            print "Try running 'make 3D' first."
        else:
            print self.threeDmodel
            plot_threeDmodel(self.threeDmodel)
