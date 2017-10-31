
import os as os
import trim as trm

"""
ADJUSTABLE "CONSTANTS"
---> These are "constants," but may be changed for the purpose of the program.
"""
# Directories
rawImagesDir = "rawImages/"
croppedImagesDir = "croppedImages/"
resizedImagesDir = "resizedImages/"

# Program Behavior
cropThresholdLevel = 125   # Higher -> Cut off more of image | Lower -> Cut off less of image | Max ~155


"""
smallestImage: accepts string which refers to a particular directory
               returns 'null' if empty or the size() attribute of the smallest image in the directory
"""
def smallestImage(directory):
    lst = os.listdir(directory)
    try:
        currentMin = lst[0]
    except:
        print "Empty directory. Cannot find smallest image."
        currentMin = 'null'

    if (currentMin != 'null'):
        for im in directory:
            if (im.size() < currentMin):
                currentMin = im.size()
                
    return currentMin


class programWrapper:
    """
    ___init___: constructor
    """
    def __init__(self):
        # do stuff
        apple = "hello"

    """
    execute: main function
    """
    def execute(self):
        # First, crop all photos
        self.__cropPhotos()
        self.__resizePhotos()

    """
    cropPhotos: crops raw photos to be approximately inline with the outline of the object
    """
    def __cropPhotos(self):
        imageList = os.listdir(rawImagesDir)
        counter = 1;
        for im in imageList:
            trm.trim(rawImagesDir + im, croppedImagesDir + "croppedIm" + str(counter) + ".jpg", cropThresholdLevel)
            counter += 1

    """
    resizePhotos: resizes all cropped images to the size of the smallest photo in croppedImagesDir
    """
    def __resizePhotos(self):
        resizeAllImagesTo = smallestImage(croppedImagesDir)
        print "Smallest Cropped Image: ", resizeAllImagesTo
