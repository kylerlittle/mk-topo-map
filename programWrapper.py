
import os as os
import trim as trm

# ADJUSTABLE "CONSTANTS"
# ---> These are "constants," but may be changed for the purpose of the program.
rawImagesDir = "rawImages/"
croppedImagesDir = "croppedImages/"


class programWrapper:
    def __init__(self):
        # do stuff
        apple = "hello"


    def execute(self):
        # First, crop all photos
        self.cropPhotos()

    def cropPhotos(self):
        imageList = os.listdir(rawImagesDir)
        counter = 1;
        for im in imageList:
            trm.trim(rawImagesDir + im, croppedImagesDir + "croppedIm" + str(counter) + ".jpg")
            counter += 1
