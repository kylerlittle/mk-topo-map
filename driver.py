"""
LIBRARIES/MODULES
"""
import programWrapper as id
import sys as sys



"""
ADJUSTABLE PARAMETERS
"""
cropThresholdLevel = 125   # Higher -> Cut off more of image | Lower -> Cut off less of image | Max ~155
widthDivisor = 10          # Higher -> Reduce size of laplacian matrix | Lower -> Retain more pixels | Min ???
heightDivisor = 10         # Higher -> Reduce size of laplacian matrix | Lower -> Retain more pixels | Min ???
startHeight = 0.0          # Height of first image taken in 'rawImages/'
endHeight = 0.1           # Height of last image taken in 'rawImages/'



"""
PROGRAM EXECUTION
"""
# Create an instance of the program driver.
driver = id.programWrapper()

# Grab the command.
try:
    command = sys.argv[1]
    print "command entered: ", command
except IndexError:
    print "No command provided."
    command = 'null'

# Execution Function: (tried to use hash map, but I'll accept losing the marginal speed gain over readability)
def executeCommand(command):
    if command == 'run':
        driver.execute(cropThresholdLevel, heightDivisor, widthDivisor, startHeight, endHeight)
    elif command == "pre_crop":
        driver.preCrop()
    elif command == 'crop':
        driver.cropPhotos(cropThresholdLevel)
    elif command == 'resize':
        driver.resizePhotos()
    elif command == 'lpc':
        driver.createLaplacianStack(heightDivisor, widthDivisor)
    elif command == '3D':
        driver.createThreeDmodel(startHeight, endHeight)
    elif command == 'o_3D':
        driver.o_createThreeDmodel(startHeight, endHeight)
    elif command == 'graph':
        driver.graphModel()
    else:
        print "Invalid Command"

# Execute the command.
if command != 'null':
    executeCommand(command)
    

