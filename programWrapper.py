
import os as os
import trim as trm
from PIL import Image

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
        # do stuff
        apple = "hello"

    """
    execute: main function
    """
    def execute(self):
        # First, crop all photos.
        self.__cropPhotos()

        # Now, resize all of the photos to the smallest image size.
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
        # now do the actual resizing
