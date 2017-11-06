
import programWrapper as id



"""
PROGRAM EXECUTION:

"""

driver = id.programWrapper()

# Crop photos
driver.cropPhotos()
print "Acceptable cropping? [Y/n]"

# If so, resize photos
driver.resizePhotos()
