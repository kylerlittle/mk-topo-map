# Installed Libraries/Modules
import os as os
from PIL import Image
from scipy import signal    # convolving operation, optimized for large matrices
import cPickle as pickle
import pylab as pl     # numpy and pyplot packaged together
import gi
gi.require_version('Vips', '8.0')       # Ensure the right version is imported
from gi.repository import Vips



# Written Libraries/Modules
import trim as trm
from Laplacian_Variance import variance_of_laplacian
from threeD_plotting import plot_threeDmodel
from parameters import parameters



# Directories
rawImagesTestDir = "raw-images-test/"
rawImagesRealDir = "../raw-images-real-1/"
croppedImagesDir = "cropped-images/"
resizedImagesDir = "resized-images/"
internalFilesDir = "wrap-internal-files/"
figuresDir = "topo-maps/"
# Internal Files
internalList = "varLpcMatrixList.pickle"
internalThreeDModel = "threeDmodel.npy"



# Program Wrapper Class
class programWrapper:
    """
    __init__: constructor
    """
    def __init__(self, parameters, testMode):
        self.resizeImagesTo = 'invalid'
        self.laplacianImageStack = []
        self.threeDmodel = 'invalid'
        self.parameters = parameters
        self.testModeOn = testMode
        self.numImages = len(os.listdir(rawImagesTestDir)) if testMode else len(os.listdir(rawImagesRealDir))

    """
    runAll: 'cropPhotos', 'resizePhotos' are run initially to determine self.resizeImagesTo; then, 'cropPhotos', 
            'resizePhotos', & 'createLaplacianStack' methods are combined to eliminate noise-reducing resampling
            and interpolating methods; lastly, model is created and graphed
    """
    def runAll(self):
        # run through the initial parts of the program in order to find resize size and check out to see if images look good enough
        self.cropPhotos()
        self.resizePhotos()
        # now process the images in place and one-by-one
        self.crop_resize_lpc()
        self.createThreeDmodel()
        self.graphModel()

    """
    cropPhotos: crops 'raw' photos to be approximately inline with the outline of the object
    """
    def cropPhotos(self):
        workingDir = rawImagesTestDir if self.testModeOn else rawImagesRealDir
        imageList = os.listdir(workingDir)
        if not imageList:
            raise SystemExit("Please populate " + workingDir + " with images. It's currently empty.")
        print "[x] Initiating image cropping"
        counter = 1;
        for imStr in imageList:
            trm.trim(workingDir + imStr, croppedImagesDir + "croppedIm" + str(counter) + ".jpg", self.parameters.mps, self.parameters.ctl, counter)
            counter += 1
                
    """
    determineResizeImagesTo: determines the smallest image in 'croppedImagesDir' & sets self.resizeImagesTo to this value
    """
    def determineResizeImagesTo(self):
        lst = os.listdir(croppedImagesDir)
        if not lst:
            raise SystemExit(croppedImagesDir + " is empty. Try running 'make crop' or 'make test_mode' first.")
        currentMin = (10000000,10000000)        # Any image should be smaller than this... otherwise, I don't want to deal with it
        for imName in lst:
            im = Image.open(croppedImagesDir + imName)
            if (im.size < currentMin):
                currentMin = im.size
            im.close()
        self.resizeImagesTo = (currentMin[0] - (currentMin[0] % self.parameters.wd), currentMin[1] - (currentMin[1] % self.parameters.wd))

    """
    resizePhotos: resizes all cropped images to the size of the smallest photo in croppedImagesDir
                  determineResizeImagesTo already checks to see if croppedImagesDir is empty
    """
    def resizePhotos(self):
        self.determineResizeImagesTo()
        imageList = os.listdir(croppedImagesDir)
        counter = 1   # utilize counter for appropriate file naming
        print "[x] Resizing all images to: ", self.resizeImagesTo
        for imStr in imageList:
            im = Image.open(croppedImagesDir + imStr)
            print "\t[", counter, "] ", im.size[0], ",", im.size[1], "resized to",
            resizedIm = im.resize(self.resizeImagesTo, resample=self.parameters.rf)
            print resizedIm.size[0], ",", resizedIm.size[1]
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
            raise SystemExit("Try running 'make resize' or 'make test_mode' first.")
        print "[x] Initiating 'variance_of_laplacian' method on resized images"
        counter = 1   # Counter included for console output
        for imStr in imageList:
            varianceMatrix = variance_of_laplacian(resizedImagesDir + imStr, self.parameters.hd, self.parameters.wd, counter)
            counter += 1  
            self.laplacianImageStack.append(varianceMatrix) # For each matrix produced from a single image, append to internal list
        with open(internalFilesDir + internalList, 'wb') as f:
            pickle.dump(self.laplacianImageStack, f, protocol=pickle.HIGHEST_PROTOCOL)
                
    """
    crop_resize_lpc: crop, resize, and create Laplacian Stack without noise-removing resampling and interpolation methods
    """
    def crop_resize_lpc(self):
        workingDir = rawImagesTestDir if self.testModeOn else rawImagesRealDir
        imageList = os.listdir(workingDir)
        if not imageList:
            raise SystemExit("Please populate 'rawImages/' with images. It's currently empty.")
        print "[x] Initiating the bulk of the program's execution (i.e. crop_resize_lpc)"
        counter = 1;
        for imStr in imageList:
            im = Vips.Image.new_from_file(workingDir + imStr)
            if im is None:
                raise SystemExit("Image to process not opened successfully.")
            if self.parameters.mps > 1.0 or self.parameters.mps <= 0.0:
                raise ValueError("You must enter a value in the interval (0.0, 1.0].")
            else:
                # Modularize crop method
                print "\t[", counter, "] ", im.width, ",", im.height, # Output image's starting size to console.
                upperEdge = int((0.5 - self.parameters.mps/2) * im.height)
                im = im.crop(0, upperEdge, im.width, im.height * self.parameters.mps)   # "Pre" cropping
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
                resizedIm = pil_img.resize(self.resizeImagesTo, resample=self.parameters.rf)
                resizedIm.save(resizedImagesDir + "readyToAnalyze" + str(counter) + ".jpg")   # save resized im to correct dir
                print resizedIm.size[0], ",", resizedIm.size[1]
                
                # Create Laplacian Stack; modularize
                print "\t[", counter, "]  Performing 'variance_of_laplacian' method on resized image...",
                Laplacian_Kernel = (pl.array([[0.,-1.,0.],[-1.,4.,-1.],[0.,-1.,0.]])) * (1./60)
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
                        varianceMatrix[subset_of_rows][subset_of_columns] = pl.var(Convolve)
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
        heightLevels = pl.linspace(0.0, abs(self.parameters.eh - self.parameters.sh), self.numImages)
        # Now, simply find max variance at each pixel 'cluster' in the stack.
        self.threeDmodel = pl.zeros(self.laplacianImageStack[0].shape)
        iterationsSinceUpdate = pl.zeros(self.laplacianImageStack[0].shape, dtype=pl.uint8) # track num iterations since updated
        print "[x] Creating 3D Model of Size",
        print "(l x w x h): ", self.threeDmodel.shape[0], "x", self.threeDmodel.shape[1], "x", self.numImages
        for index, laplacianOfImMatrix in enumerate(self.laplacianImageStack):
            pointsInFocus = 0
            for row in pl.arange(laplacianOfImMatrix.shape[0]):
                for col in pl.arange(laplacianOfImMatrix.shape[1]):
                    if laplacianOfImMatrix[row][col] > self.threeDmodel[row][col] and iterationsSinceUpdate[row][col] < self.parameters.mai + 1:   # add one so that self.parameters.mai iterations actually pass before cell is blocked
                        pointsInFocus += 1
                        self.threeDmodel[row][col] = heightLevels[index]
                        if index > 0:
                            iterationsSinceUpdate[row][col] = 1
                    else:
                        if iterationsSinceUpdate[row][col] != 0:      # make sure cell has stopped being updated BEYOND first iteration
                            iterationsSinceUpdate[row][col] += 1
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
                        self.__createThreeDmodel__()
                    except IOError:
                        print "Error reading ", internalList
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
                        plot_threeDmodel(self.threeDmodel, self.parameters.du, figuresDir, self.parameters, self.testModeOn)
                    except IOError:
                        print "Error reading", internalThreeDModel
        except OSError:
            print "Try running 'make 3D' first."
