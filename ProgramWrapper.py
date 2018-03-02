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
import trim
import variance_of_laplacian
from three_d_plotting import plot_three_d_model
import parameters



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
class ProgramWrapper:
    def __init__(self, parameters, testmode=True):
        """
        __init__: constructor
        """
        self.ResizeImagesSize = 'invalid'
        self.VoLImageStack = []
        self.ThreeDModel = 'invalid'
        self.Parameters = parameters
        self.TestModeOn = testmode
        self.NumImages = len(os.listdir(rawImagesTestDir)) if testmode else len(os.listdir(rawImagesRealDir))

    def run_program(self):
        """
        run_program: 'crop_photos', 'resize_photos' are run initially to determine self.ResizeImagesSize; then, 'crop_photos', 
                'resize_photos', & 'createLaplacianStack' methods are combined to eliminate noise-reducing resampling
                and interpolating methods; lastly, model is created and graphed
        """
        # run through the initial parts of the program in order to find resize size and check out to see if images look good enough
        self.crop_photos()
        self.resize_photos()
        # now process the images in place and one-by-one
        self.crop_resize_vol()
        self.create_three_d_model()
        self.graph_model()


    def crop_photos(self):
        """
        crop_photos: crops 'raw' photos to be approximately inline with the outline of the object
        """
        workingDir = rawImagesTestDir if self.TestModeOn else rawImagesRealDir
        imageList = os.listdir(workingDir)
        if not imageList:
            raise SystemExit("Please populate " + workingDir + " with images. It's currently empty.")
        print "[x] Initiating image cropping"
        counter = 1;
        for imStr in imageList:
            trim.trim(workingDir + imStr, croppedImagesDir + "croppedIm" + str(counter) + ".jpg", self.Parameters.mps, self.Parameters.ctl, counter)
            counter += 1
                
    def determineResizeImagesTo(self):
        """
        determineResizeImagesTo: determines the smallest image in 'croppedImagesDir' & sets self.ResizeImagesSize to this value
        """
        lst = os.listdir(croppedImagesDir)
        if not lst:
            raise SystemExit(croppedImagesDir + " is empty. Try running 'make crop' or 'make test_mode' first.")
        currentMin = (10000000,10000000)        # Any image should be smaller than this... otherwise, I don't want to deal with it
        for imName in lst:
            im = Image.open(croppedImagesDir + imName)
            if (im.size < currentMin):
                currentMin = im.size
            im.close()
        self.ResizeImagesSize = (currentMin[0] - (currentMin[0] % self.Parameters.wd), currentMin[1] - (currentMin[1] % self.Parameters.wd))

    def resize_photos(self):
        """Resize all images to the size of the smallest photo in croppedImagesDir."""
        self.determineResizeImagesTo()
        imageList = os.listdir(croppedImagesDir)
        counter = 1   # utilize counter for appropriate file naming
        print "[x] Resizing all images to: ", self.ResizeImagesSize
        for imStr in imageList:
            im = Image.open(croppedImagesDir + imStr)
            print "\t[", counter, "] ", im.size[0], ",", im.size[1], "resized to",
            resizedIm = im.resize(self.ResizeImagesSize, resample=self.Parameters.rf)
            print resizedIm.size[0], ",", resizedIm.size[1]
            resizedIm.save(resizedImagesDir + "readyToAnalyze" + str(counter) + ".jpg")   # save resized im to correct dir
            im.close()
            counter += 1

    def createLaplacianStack(self):
        """
        createLaplacianStack: for each image in 'resizedImagesDir/', calculate its variance
        of laplacian matrix; append to internal list; write list to
        file for further use
        """
        imageList = os.listdir(resizedImagesDir)
        if not imageList:
            raise SystemExit("Try running 'make resize' or 'make test_mode' first.")
        print "[x] Initiating 'variance_of_laplacian' method on resized images"
        counter = 1   # Counter included for console output
        for imStr in imageList:
            varianceMatrix = variance_of_laplacian(resizedImagesDir + imStr, self.Parameters.hd, self.Parameters.wd, counter)
            counter += 1  
            self.VoLImageStack.append(varianceMatrix) # For each matrix produced from a single image, append to internal list
        with open(internalFilesDir + internalList, 'wb') as f:
            pickle.dump(self.VoLImageStack, f, protocol=pickle.HIGHEST_PROTOCOL)
                
    def crop_resize_vol(self):
        """
        crop_resize_vol: crop, resize, and create Laplacian Stack without noise-removing resampling and interpolation methods
        """
        workingDir = rawImagesTestDir if self.TestModeOn else rawImagesRealDir
        imageList = os.listdir(workingDir)
        if not imageList:
            raise SystemExit("Please populate 'rawImages/' with images. It's currently empty.")
        print "[x] Initiating the bulk of the program's execution (i.e. crop_resize_vol)"
        counter = 1;
        for imStr in imageList:
            im = Vips.Image.new_from_file(workingDir + imStr)
            if im is None:
                raise SystemExit("Image to process not opened successfully.")
            elif self.Parameters.mps > 1.0 or self.Parameters.mps <= 0.0:
                raise ValueError("You must enter a value in the interval (0.0, 1.0].")
            else:
                # Modularize crop method
                print "\t[", counter, "] ", im.width, ",", im.height, # Output image's starting size to console.
                upperEdge = int((0.5 - self.Parameters.mps/2) * im.height)
                im = im.crop(0, upperEdge, im.width, im.height * self.Parameters.mps)   # "Pre" cropping
                background = im.getpoint(0, 0)
                mask = (im.median(3) - background).abs() > self.Parameters.ctl
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
                resizedIm = pil_img.resize(self.ResizeImagesSize, resample=self.Parameters.rf)
                resizedIm.save(resizedImagesDir + "readyToAnalyze" + str(counter) + ".jpg")   # save resized im to correct dir
                print resizedIm.size[0], ",", resizedIm.size[1]
                
                # Create Laplacian Stack; modularize
                print "\t[", counter, "]  Performing 'variance_of_laplacian' method on resized image...",
                Laplacian_Kernel = (pl.array([[0.,-1.,0.],[-1.,4.,-1.],[0.,-1.,0.]])) * (1./60)
                miniMatrix = pl.zeros((self.Parameters.hd,self.Parameters.wd)) # heightDivisor x widthDivisor Matrix to copy elements to
                varianceMatrix = pl.zeros((resizedIm.size[1] / self.Parameters.hd, resizedIm.size[0] / self.Parameters.wd))
                imageMatrix = pl.asarray(resizedIm.convert('L')) # convert image to greyscale; return matrix
                for subset_of_rows in pl.arange(resizedIm.size[1] / self.Parameters.hd):  # TOTAL Image Matrix
                    for subset_of_columns in pl.arange(resizedIm.size[0] / self.Parameters.wd):
                        image_row = subset_of_rows * self.Parameters.hd # keeps track of larger matrix's row index to copy from  
                        image_col = subset_of_columns * self.Parameters.wd # keeps track of larger matrix's dolumn index to copy from
                        for row in pl.arange(self.Parameters.hd):
                            for col in pl.arange(self.Parameters.wd):
                                miniMatrix[row][col] = imageMatrix[image_row + row][image_col + col]
                        Convolve = signal.fftconvolve(miniMatrix, Laplacian_Kernel, mode='full')
                        varianceMatrix[subset_of_rows][subset_of_columns] = pl.var(Convolve)
                print "Done."
                
                # Append to internal laplacian stack; modularize
                self.VoLImageStack.append(varianceMatrix)
            # Lastly, update counter
            counter += 1                        
        # After all of that, finally just dump it to a file
        with open(internalFilesDir + internalList, 'wb') as f:
            pickle.dump(self.VoLImageStack, f, protocol=pickle.HIGHEST_PROTOCOL)
                
    def __create_three_d_model__(self):
        """
        __create_three_d_model__: helper function for create_three_d_model
        """
        heightLevels = pl.linspace(0.0, abs(self.Parameters.eh - self.Parameters.sh), self.NumImages)
        # Now, simply find max variance at each pixel 'cluster' in the stack.
        self.ThreeDModel = pl.zeros(self.VoLImageStack[0].shape)
        iterationsSinceUpdate = pl.zeros(self.VoLImageStack[0].shape, dtype=pl.uint8) # track num iterations since updated
        print "[x] Creating 3D Model of Size",
        print "(l x w x h): ", self.ThreeDModel.shape[0], "x", self.ThreeDModel.shape[1], "x", self.NumImages
        for index, laplacianOfImMatrix in enumerate(self.VoLImageStack):
            pointsInFocus = 0
            for row in pl.arange(laplacianOfImMatrix.shape[0]):
                for col in pl.arange(laplacianOfImMatrix.shape[1]):
                    if laplacianOfImMatrix[row][col] > self.ThreeDModel[row][col] and iterationsSinceUpdate[row][col] < self.Parameters.mai + 1:   # add one so that self.Parameters.mai iterations actually pass before cell is blocked
                        pointsInFocus += 1
                        self.ThreeDModel[row][col] = heightLevels[index]
                        if index > 0:
                            iterationsSinceUpdate[row][col] = 1
                    else:
                        if iterationsSinceUpdate[row][col] != 0:      # make sure cell has stopped being updated BEYOND first iteration
                            iterationsSinceUpdate[row][col] += 1
            print "\t[", index + 1, "] Percentage of Pixel Clusters Updated: ", pointsInFocus, "/", laplacianOfImMatrix.size, "=",
            print float(pointsInFocus) / laplacianOfImMatrix.size
        # This time, store results using numpy since we're dealing with an array object
        with open(internalFilesDir + internalThreeDModel, 'wb') as f:
            pl.save(f, self.ThreeDModel)
            
    def create_three_d_model(self):
        """
        create_three_d_model: endHeight & startHeight are assumed to be nonnegative
        otherwise, error checking is performed
        Finds maxVariance at a particular 'cluster' (heightDivisor x widthDivisor) of pixels &
        stores the height that this occurred at in self.ThreeDModel
        """
        try:
            assert isinstance(self.Parameters.sh, float) == True
            assert isinstance(self.Parameters.eh, float) == True
        except AssertionError:
            print "One or more of 'startHeight' and 'endHeight' are not floating point values."

        try:
            if os.stat(internalFilesDir + internalList).st_size > 0:  # checks for empty file; if so, OSError thrown
                with open(internalFilesDir + internalList, 'rb') as f:
                    try:
                        self.VoLImageStack = pickle.load(f)
                        self.__create_three_d_model__()
                    except IOError:
                        print "Error reading ", internalList
        except OSError:
            print "Try running 'make lpc' first."
            
    def o_create_three_d_model(self):
        """
        o_create_three_d_model: same as create_three_d_model, but breaks once values begin to descend
        'o' stands for optimized; works because of the physics of optics
        """
        pass

    def graph_model(self):
        """
        graph_model: plots the graph produced & displays to screen
        """
        try:
            if os.stat(internalFilesDir + internalThreeDModel).st_size > 0:  # checks for empty file; if so, OSError thrown
                with open(internalFilesDir + internalThreeDModel, 'rb') as f:    # handles open, close, and errors with opening
                    try:   # If file doesn't load correctly, IOError is thrown.
                        self.ThreeDModel = pl.load(f)
                        plot_three_d_model(self.ThreeDModel, self.Parameters.du, figuresDir, self.Parameters, self.TestModeOn)
                    except IOError:
                        print "Error reading", internalThreeDModel
        except OSError:
            print "Try running 'make 3D' first."
