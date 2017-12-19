"""
LIBRARIES/MODULES
"""
import programWrapper as id
import sys as sys



"""
ADJUSTABLE PARAMETERS
"""
middlePercentSaving = 0.5  # Save middle x% of images | Accepted Values in Interval: (0.0, 1.0]
cropThresholdLevel = 125   # Higher -> Cut off more of image | Lower -> Cut off less of image | Max ~155
widthDivisor = 10          # Higher -> Reduce size of laplacian matrix | Lower -> Retain more pixels | Min ???
heightDivisor = 10         # Higher -> Reduce size of laplacian matrix | Lower -> Retain more pixels | Min ???
startHeight = 110.7        # Height of first image taken in 'rawImages/'
endHeight = 149.6          # Height of last image taken in 'rawImages/'
dimension_units = 'mm'     # Currently supports: in, mm, and cm



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
    if command == 'all':
        driver.runAll(middlePercentSaving, cropThresholdLevel, heightDivisor, widthDivisor, startHeight, endHeight, dimension_units)
    elif command == 'run':
        driver.execute(middlePercentSaving, cropThresholdLevel, heightDivisor, widthDivisor, startHeight, endHeight, dimension_units)
    elif command == 'crop':
        driver.cropPhotos(middlePercentSaving, cropThresholdLevel)
    elif command == 'resize':
        driver.resizePhotos()
    elif command == 'lpc':
        driver.createLaplacianStack(heightDivisor, widthDivisor)
    elif command == '3D':
        driver.createThreeDmodel(startHeight, endHeight)
    elif command == 'o_3D':
        driver.o_createThreeDmodel(startHeight, endHeight)
    elif command == 'graph':
        driver.graphModel(dimension_units)
    else:
        print "Invalid Command"

# Execute the command.
if command != 'null':
    executeCommand(command)
    

