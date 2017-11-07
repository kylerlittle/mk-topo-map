
import programWrapper as id
import sys as sys

"""
ADJUSTABLE PARAMETERS
---> These are parameters which may be altered to produce new results.
"""
cropThresholdLevel = 125   # Higher -> Cut off more of image | Lower -> Cut off less of image | Max ~155
widthDivisor = 10          # Higher -> Reduce size of laplacian matrix | Lower -> Retain more pixels | Min ???
heightDivisor = 10          # Higher -> Reduce size of laplacian matrix | Lower -> Retain more pixels | Min ???




"""
PROGRAM EXECUTION:
"""
driver = id.programWrapper()

# Grab command
try:
    command = sys.argv[1]
    print "command entered: ", command
except IndexError:
    print "No command provided."
    command = 'null'

def executeCommand(command):
    if command == 'run':
        driver.execute(cropThresholdLevel)
    elif command == 'crop':
        driver.cropPhotos(cropThresholdLevel)
    elif command == 'resize':
        driver.resizePhotos()
    elif command == 'lpc':
        print "Laplacian unimplemented."
    elif command == 'graph':
        print "Graph unimplemented."
    else:
        print "Invalid Command"

if command != 'null':
    executeCommand(command)
    

