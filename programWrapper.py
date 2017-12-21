# Libraries/Modules
import os as os
import trim as trm
from PIL import Image
from Laplacian_Variance import variance_of_laplacian
from threeD_plotting import plot_threeDmodel
from crop_resize_lpc import crop_resize_lpc
import cPickle as pickle
import numpy as np
import gi
gi.require_version('Vips', '8.0')       # Ensure the right version is imported
from gi.repository import Vips

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
        self.crop_resize_lpc(middlePercentSaving, cropThresholdLevel, heightDivisor, widthDivisor)
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
    crop_resize_lpc: crop, resize, and create Laplacian Stack without a single image write
    """
    def crop_resize_lpc(self, middlePercentSaving, cropThresholdLevel, heightDivisor, widthDivisor):
        Laplacian_Kernel = (pl.array([[0.,-1.,0.],[-1.,4.,-1.],[0.,-1.,0.]])) * (1./60)
        imageList = os.listdir(rawImagesDir)
        if not imageList:
            print "Please populate 'rawImages/' with images."
        else:
            print "[x] Initiating image cropping"
            couter = 1;
            for imStr in imageList:
                im = Vips.Image.new_from_file(rawImagesDir + imStr)
                if (im != NULL):       # Image provided & opened successfully.
                    print "\t[", counter, "] ", im.width, ",", im.height, # Output image's starting size to console.
                    if middlePercentSaving > 1.0 or middlePercentSaving <= 0.0:
                        raise ValueError("You must enter a value in the interval (0.0, 1.0].")
                    else:
                        # Modularize this...
                        upper = int((0.5 - middlePercentSaving/2) * im.height); lower = int((0.5 + middlePercentSaving/2) * im.height)
                        im = im.crop(0, upper, im.width, lower) # "Pre" cropping the image to ignore a few dumb things in the lab.
                        background = im.getpoint(0, 0)
                        mask = (im.median(3) - background).abs() > acceptableThreshold
                        columns, rows = mask.project()
                        left = columns.profile()[1].min()
                        right = columns.width - columns.flip("horizontal").profile()[1].min()
                        top = rows.profile()[0].min()
                        bottom = rows.height - rows.flip("vertical").profile()[0].min()
                        im = im.crop(left, top, right - left, bottom - top)
                        print "cropped to", im.width, ",", im.height     # Output ending size to the console

                        # Resize... use VIPS version. Modularize this part too.
                        # Note, will need to get self.smallestImage by doing a pre processing...
                        print "\t[", counter, "] ", im.size[0], ",", im.size[1], "resized to",
                        resizedIm = im.resize(self.smallestImage, resample=Image.LANCZOS)    # resize using LANCZOS filtering
                        print resizedIm.size[0], ",", resizedIm.size[1]

                        # Create Laplacian Stack; modularize
                        totalImageRows = pl.arange(im.height / heightDivisor)
                        totalImageColumns = pl.arange(im.width / widthDivisor)
                        numRows_MiniMatrix = pl.arange(heightDivisor)
                        numCols_MiniMatrix = pl.arange(widthDivisor)
                        miniMatrix = pl.zeros((heightDivisor,widthDivisor)) # heightDivisor x widthDivisor Matrix to copy elements to
                        varianceMatrix = pl.zeros((im.height / heightDivisor, im.width / widthDivisor))
                        toBeConverted = toBeConverted.resize([(im.width / widthDivisor) * widthDivisor,(im.height / heightDivisor) * heightDivisor], resample=Image.LANCZOS)    # resize using LANCZOS filtering        
                        # truncating the width and height so that they're divisible by heightDivisor & widthDivisor                    
                        imageMatrix = pl.asarray(toBeConverted.convert('L')) # convert image to greyscale; return matrix                 
                        print "\t[", counter, "] Convolving subdivisions of image with Laplacian Kernel... Calculating Variance... ",
                        for subset_of_rows in totalImageRows:  # TOTAL Image Matrix
                            for subset_of_columns in totalImageColumns:
                                image_row = subset_of_rows * heightDivisor # keeps track of larger matrix's row index to copy from      
                                image_col = subset_of_columns * widthDivisor # keeps track of larger matrix's dolumn index to copy from
                                for row in numRows_MiniMatrix:
                                    for col in numCols_MiniMatrix:
                                        miniMatrix[row][col] = imageMatrix[image_row + row][image_col + col]
                            Convolve = signal.fftconvolve(miniMatrix, Laplacian_Kernel, mode='full')
                            Variance = pl.var(Convolve)
                            varianceMatrix[subset_of_rows][subset_of_columns] = Variance
                        print "Done."

                        # Append to internal laplacian stack; modularize
                        self.laplacianImageStack.append(varianceMatrix) # For each matrix produced from a single image, append to internal list
                    # After all of that, finally just dump it to a file
                    with open(internalList, 'wb') as f:
                        pickle.dump(self.laplacianImageStack, f, protocol=pickle.HIGHEST_PROTOCOL)
                else:
                    print "Image to process not opened successfully."
                
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
