# Installed Libraries/Modules
import os as os
import trim as trm
from PIL import Image
from scipy import signal    # convolving operation, optimized for large matrices
import cPickle as pickle
import pylab as pl     # numpy and pyplot packaged together
import gi
gi.require_version('Vips', '8.0')       # Ensure the right version is imported
from gi.repository import Vips
# Written Libraries/Modules
from Laplacian_Variance import variance_of_laplacian
from threeD_plotting import plot_threeDmodel
from parameters import parameters

# Directories
rawImagesDir = "../raw-images-test-1/"   # "raw-images/" 
croppedImagesDir = "cropped-images/"
resizedImagesDir = "resized-images/"
internalFilesDir = "wrap-internal-files/"
figuresDir = "topo-maps/"
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
    __init__: constructor
    """
    def __init__(self, parameters):
        self.smallestImageSize = 'invalid'
        self.resizeImagesTo = 'invalid'
        self.laplacianImageStack = []
        self.numImages = len(os.listdir(rawImagesDir))
        self.threeDmodel = 'invalid'
        self.parameters = parameters

    """
    runAll: same as 'execute' but with 'cropPhotos', 'resizePhotos', & 'createLaplacianStack' methods combined
    """
    def runAll(self):
        # run through the initial parts of the program in order to find resize size (i.e. self.smallestImageSize)
        self.cropPhotos()
        self.resizePhotos()
        # now process the images in place and one-by-one
        self.crop_resize_lpc()
        self.createThreeDmodel()
        self.graphModel()
    
    """
    execute: main function to execute all tasks in one (CAREFUL WITH THIS)
             by default, createThreeDmodel is used rather than optimized version
    """
    def execute(self):
        self.cropPhotos()
        self.resizePhotos()
        self.createLaplacianStack()
        self.createThreeDmodel()
        self.graphModel()

    """
    cropPhotos: crops 'raw' photos to be approximately inline with the outline of the object
    """
    def cropPhotos(self):
        imageList = os.listdir(rawImagesDir)
        if not imageList:
            print "Please populate 'rawImages/' with images."
        else:
#           print "[x] Initiating image cropping"
            counter = 1;
            for imStr in imageList:
                trm.trim(rawImagesDir + imStr, croppedImagesDir + "croppedIm" + str(counter) + ".jpg", self.parameters.mps, self.parameters.ctl, counter)
                counter += 1

    """
    resizePhotos: resizes all cropped images to the size of the smallest photo in croppedImagesDir
                  LANCZOS filtering was chosen so as to retain highest downscaling quality
                  performance is least important in this case, so we sacrifice it
    """
    def resizePhotos(self):
        self.smallestImageSize = smallestImage(croppedImagesDir)
        imageList = os.listdir(croppedImagesDir)
        if not imageList:
            print "Try running 'make crop' first."
        else:
            counter = 1   # utilize counter for appropriate file naming
#           print "[x] Resizing all images to: ", self.smallestImageSize
            for imStr in imageList:
                im = Image.open(croppedImagesDir + imStr)
                #print "\t[", counter, "] ", im.size[0], ",", im.size[1], "resized to",
                resizedIm = im.resize(self.smallestImageSize, resample=Image.LANCZOS)    # resize using LANCZOS filtering
                #print resizedIm.size[0], ",", resizedIm.size[1]
                resizedIm.save(resizedImagesDir + "readyToAnalyze" + str(counter) + ".jpg")   # save resized im to correct dir
                im.close()
                counter += 1

    """
    createLaplacianStack: for each image in 'resizedImagesDir/', calculate its variance
                          of laplacian matrix; append to internal list; write list to
                          file for further use
    """
    def createLaplacianStack(self):
        imageList = os.listdir(resizedImagesDir)
        if not imageList:
            print "Try running 'make resize' first."
        else:
            print "[x] Initiating 'variance_of_laplacian' method on resized images"
            counter = 1   # Counter included for console output
            for imStr in imageList:
                varianceMatrix = variance_of_laplacian(resizedImagesDir + imStr, self.parameters.hd, self.parameters.wd, counter)
                counter += 1  
                self.laplacianImageStack.append(varianceMatrix) # For each matrix produced from a single image, append to internal list
            with open(internalFilesDir + internalList, 'wb') as f:
                pickle.dump(self.laplacianImageStack, f, protocol=pickle.HIGHEST_PROTOCOL)
                
    """
    crop_resize_lpc: crop, resize, and create Laplacian Stack without a single image write
    """
    def crop_resize_lpc(self):
        Laplacian_Kernel = (pl.array([[0.,-1.,0.],[-1.,4.,-1.],[0.,-1.,0.]])) * (1./60)
        self.resizeImagesTo = (self.smallestImageSize[0] - (self.smallestImageSize[0] % self.parameters.wd), self.smallestImageSize[1] - (self.smallestImageSize[1] % self.parameters.wd))
        imageList = os.listdir(rawImagesDir)
        if not imageList:
            print "Please populate 'rawImages/' with images."
        else:
            counter = 1;
            for imStr in imageList:
                im = Vips.Image.new_from_file(rawImagesDir + imStr)
                if im is None:
                    print "Image to process not opened successfully."
                else:       # Image provided & opened successfully.
                    print "\t[", counter, "] ", im.width, ",", im.height, # Output image's starting size to console.
                    if self.parameters.mps > 1.0 or self.parameters.mps <= 0.0:
                        raise ValueError("You must enter a value in the interval (0.0, 1.0].")
                    else:
                        # Modularize this...
                        upper = int((0.5 - self.parameters.mps/2) * im.height); lower = int((0.5 + self.parameters.mps/2) * im.height)
                        im = im.crop(0, upper, im.width, lower) # "Pre" cropping the image to ignore a few dumb things in the lab.
                        background = im.getpoint(0, 0)
                        mask = (im.median(3) - background).abs() > self.parameters.ctl
                        columns, rows = mask.project()
                        left = columns.profile()[1].min()
                        right = columns.width - columns.flip("horizontal").profile()[1].min()
                        top = rows.profile()[0].min()
                        bottom = rows.height - rows.flip("vertical").profile()[0].min()
                        im = im.crop(left, top, right - left, bottom - top)
                        print "cropped to", im.width, ",", im.height     # Output ending size to the console
                        # Convert to PIL image; modularize...
                        mem_img = im.write_to_memory()
                        pil_img = Image.fromarray(pl.fromstring(mem_img, dtype=pl.uint8).reshape(im.height, im.width, im.bands), mode='RGB')
                        # Resize PIL image
                        print "\t[", counter, "] ", pil_img.size[0], ",", pil_img.size[1], "resized to",
                        resizedIm = pil_img.resize(self.resizeImagesTo, resample=Image.NEAREST)
                        resizedIm.save(resizedImagesDir + "readyToAnalyze" + str(counter) + ".jpg")   # save resized im to correct dir
                        print resizedIm.size[0], ",", resizedIm.size[1]
                        # Create Laplacian Stack; modularize
                        print "\t[", counter, "]  Performing 'variance_of_laplacian' method on resized image...",
                        miniMatrix = pl.zeros((self.parameters.hd,self.parameters.wd)) # heightDivisor x widthDivisor Matrix to copy elements to
                        varianceMatrix = pl.zeros((resizedIm.size[1] / self.parameters.hd, resizedIm.size[0] / self.parameters.wd))
                        imageMatrix = pl.asarray(resizedIm.convert('L')) # convert image to greyscale; return matrix
                        for subset_of_rows in pl.arange(resizedIm.size[1] / self.parameters.hd):  # TOTAL Image Matrix
                            for subset_of_columns in pl.arange(resizedIm.size[0] / self.parameters.wd):
                                image_row = subset_of_rows * self.parameters.hd # keeps track of larger matrix's row index to copy from      
                                image_col = subset_of_columns * self.parameters.wd # keeps track of larger matrix's dolumn index to copy from
                                for row in pl.arange(self.parameters.hd):
                                    for col in pl.arange(self.parameters.wd):
                                        miniMatrix[row][col] = imageMatrix[image_row + row][image_col + col]
                                Convolve = signal.fftconvolve(miniMatrix, Laplacian_Kernel, mode='full')
                                Variance = pl.var(Convolve)
                                varianceMatrix[subset_of_rows][subset_of_columns] = Variance
                        print "Done."
                        # Append to internal laplacian stack; modularize
                        self.laplacianImageStack.append(varianceMatrix)
                        # Lastly, update counter
                        counter += 1                        
        # After all of that, finally just dump it to a file
        with open(internalFilesDir + internalList, 'wb') as f:
            pickle.dump(self.laplacianImageStack, f, protocol=pickle.HIGHEST_PROTOCOL)
                
    """
    __createThreeDmodel__: helper function for createThreeDmodel
    """
    def __createThreeDmodel__(self):
        heightLevels = pl.linspace(0.0, abs(self.parameters.eh - self.parameters.sh), self.numImages) # by default, linspace includes endpoint
        # Now, simply find max variance at each pixel 'cluster' in the stack.
        self.threeDmodel = pl.zeros(self.laplacianImageStack[0].shape)
        print "[x] Creating 3D Model of Size",
        print "(l x w x h): ", self.threeDmodel.shape[0], "x", self.threeDmodel.shape[1], "x", self.numImages
        for index, laplacianOfImMatrix in enumerate(self.laplacianImageStack):
            pointsInFocus = 0
            for row in pl.arange(laplacianOfImMatrix.shape[0]):
                for col in pl.arange(laplacianOfImMatrix.shape[1]):
                    if laplacianOfImMatrix[row][col] > self.threeDmodel[row][col]:
                        pointsInFocus += 1
                        self.threeDmodel[row][col] = heightLevels[index]
            print "\t[", index + 1, "] Percentage of Pixel Clusters Updated: ", pointsInFocus, "/", laplacianOfImMatrix.size, "=",
            print float(pointsInFocus) / laplacianOfImMatrix.size
        # This time, store results using numpy since we're dealing with an array object
        with open(internalFilesDir + internalThreeDModel, 'wb') as f:
            pl.save(f, self.threeDmodel)
            
    """
    createThreeDmodel: endHeight & startHeight are assumed to be nonnegative
                       otherwise, error checking is performed
                       Finds maxVariance at a particular 'cluster' (heightDivisor x widthDivisor) of pixels &
                       stores the height that this occurred at in self.threeDmodel
    """
    def createThreeDmodel(self):
        try:
            assert isinstance(self.parameters.sh, float) == True
            assert isinstance(self.parameters.eh, float) == True
        except AssertionError:
            print "One or more of 'startHeight' and 'endHeight' are not floating point values."

        try:
            if os.stat(internalFilesDir + internalList).st_size > 0:  # checks for empty file; if so, OSError thrown
                with open(internalFilesDir + internalList, 'rb') as f:
                    try:
                        self.laplacianImageStack = pickle.load(f)
                        self.smallestImageSize = smallestImage(croppedImagesDir)   # If not running 'execute', this needs to be updated
                        self.__createThreeDmodel__()
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
    def graphModel(self):
        try:
            if os.stat(internalFilesDir + internalThreeDModel).st_size > 0:  # checks for empty file; if so, OSError thrown
                with open(internalFilesDir + internalThreeDModel, 'rb') as f:    # handles open, close, and errors with opening
                    try:   # If file doesn't load correctly, IOError is thrown.
                        self.threeDmodel = pl.load(f)
                        plot_threeDmodel(self.threeDmodel, self.parameters.du, figuresDir, self.parameters)
                    except IOError:
                        print "Error reading", internalThreeDModel
        except OSError:
            print "Try running 'make 3D' first."
