
import os as os
import trim as trm
from PIL import Image
from Laplacian_Variance import variance_of_laplacian

# Directories
rawImagesDir = "rawImages/"
croppedImagesDir = "croppedImages/"
resizedImagesDir = "resizedImages/"

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
        # Initialize size to be (numImages * widthDivisor * heightDivisor)
        laplacian3Dmatrix = 'unimplemented'

    """
    execute: main function to execute all tasks in one (CAREFUL WITH THIS)
    """
    def execute(self, cropThresholdLevel):
        self.cropPhotos(cropThresholdLevel)
        self.resizePhotos()

    """
    cropPhotos: crops raw photos to be approximately inline with the outline of the object
    """
    def cropPhotos(self, cropThresholdLevel):
        print "[x] Initiating image cropping"
        imageList = os.listdir(rawImagesDir)
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
        counter = 1   # utilize counter for appropriate file naming
        print "[x] Resizing all images to: ", resizeAllImagesTo
        for imStr in imageList:
            im = Image.open(croppedImagesDir + imStr)
            resizedIm = im.resize(resizeAllImagesTo, resample=Image.LANCZOS)    # resize using LANCZOS filtering
            resizedIm.save(resizedImagesDir + "readyToAnalyze" + str(counter) + ".jpg")   # save resized im to correct dir
            im.close()
            counter += 1

    """
    foo: 
    """
    def foo(self):
        imageList = os.listdir(resizedImagesDir)
        for imStr in imageList:
            varianceMatrix = variance_of_laplacian(imStr, heightDivisor, widthDivisor)
            laplacian3Dmatrix.append(varianceMatrix)
            # For each matrix in laplacian3DMatrix, push each entry onto a list, 

            
            
        
