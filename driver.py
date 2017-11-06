
import programWrapper as id
import sys as sys

"""
ADJUSTABLE "CONSTANTS"
---> These are "constants," but may be changed for the purpose of the program.
"""
cropThresholdLevel = 125   # Higher -> Cut off more of image | Lower -> Cut off less of image | Max ~155
"""
Once I get real data, I need to do tests to determine best output. Vary widthDivisor & heightDivisor accordingly
"""
widthDivisor = 10          # Higher -> Reduce size of laplacian matrix | Lower -> Retain more pixels | Min ???
heightDivisor = 10          # Higher -> Reduce size of laplacian matrix | Lower -> Retain more pixels | Min ???


"""
PROGRAM EXECUTION:

"""


driver = id.programWrapper()
try:
    command = sys.argv[1]
except IndexError:
    print "No command provided."

def a():
    print "Laplacian unimplemented."

def b():
    print "Graph unimplemented."

switchFunction = {
    "crop": driver.cropPhotos(),
    "resize": driver.resizePhotos(),
    "lpc" : a(),
    "graph": b()
}

try:
    switchFunction[command]
except KeyError:
    print "Invalid Command."


