"""
LIBRARIES/MODULES
"""
import programWrapper as id
import sys as sys
from parameters import parameters



"""
TEST PARAMETERS
mps=0.5     # Save middle x% of images | Accepted Values in Interval: (0.0, 1.0]
ctl=125     # Higher -> Cut off more of image | Lower -> Cut off less of image | Max ~155
wd=10       # Higher -> Reduce size of laplacian matrix | Lower -> Retain more pixels | Min ???
hd=10       # Higher -> Reduce size of laplacian matrix | Lower -> Retain more pixels | Min ???
sh=110.7    # Height of first image taken in 'rawImages/'
eh=149.6    # Height of last image taken in 'rawImages/'
du='mm'     # Currently supports: in, mm, and cm
"""
test_parameters = parameters(0.5, 125, 10, 10, 110.7, 149.6, 'mm')



"""
PROGRAM EXECUTION
"""
# Create an instance of the program driver.
driver = id.programWrapper(test_parameters)

# Grab the command.
try:
    command = sys.argv[1]
    print "command entered: ", command
except IndexError:
    print "No command provided."
    command = 'null'

# Execution Function:
def executeCommand(command):
    if command == 'all':
        driver.runAll()
    elif command == 'crop':
        driver.cropPhotos()
    elif command == 'resize':
        driver.resizePhotos()
    elif command == 'lpc':
        driver.createLaplacianStack()
    elif command == '3D':
        driver.createThreeDmodel()
    elif command == 'o_3D':
        driver.o_createThreeDmodel()
    elif command == 'graph':
        driver.graphModel()
    else:
        print "Invalid Command"

# Execute the command.
if command != 'null':
    executeCommand(command)
