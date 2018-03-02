"""
LIBRARIES/MODULES
"""
import ProgramWrapper as pw
import sys as sys
from parameters import parameters
import numpy as np
from PIL import Image



"""
HOW TO VARY PARAMETERS (you can change these as you see fit)
"""
whd_range = (8, 14)     # vary the width & height divisors from whd_range[0] to whd_range[1] in increments of whd_step
whd_step = 1
mps_range = (0.25, 0.75)   # vary the middle percent savings from mps_range[0] to mps_range[1] in increments of mps_step
mps_step = .10
mai_range = (3, 6)    # vary the maximum allowable iterations from mai_range[0] to mai_range[1] in increments of mai_step
mai_step = 1
rf_num = 4      # Number of resizing filters... NEAREST = 0, BILINEAR = 1, BICUBIC = 2, LANCZOS = 3



"""
CLASS WRAPPER
"""
class VaryParameters:
    def __init__(self, whd_range, whd_step, mps_range, mps_step, mai_range, mai_step, rf_num):
        self.whd_range = whd_range
        self.whd_step = whd_step
        self.mps_range = mps_range
        self.mps_step = mps_step
        self.mai_range = mai_range
        self.mai_step = mai_step
        self.rf_num = rf_num
        
    def width_height_divisors(self):
        for val in np.arange(self.whd_range[0], self.whd_range[1], self.whd_step):
            params = parameters(0.5, 125, Image.NEAREST, val, val, 110.7, 149.6, 5, 'mm')
            program = pw.ProgramWrapper(params, testmode=False)
            program.run_program()
        
    def mid_perecent_save(self):
        for val in np.arange(self.mps_range[0], self.mps_range[1], self.mps_step):
            params = parameters(val, 125, Image.NEAREST, 10, 10, 110.7, 149.6, 5, 'mm')
            program = pw.ProgramWrapper(params, testmode=False)
            program.run_program()

    def vary_whd_mps(self):
        for whd_val in np.arange(self.whd_range[0], self.whd_range[1], self.whd_step):
            for mps_val in np.arange(self.mps_range[0], self.mps_range[1], self.mps_step):
                params = parameters(mps_val, 125, Image.NEAREST, whd_val, whd_val, 110.7, 149.6, 5, 'mm')
                program = pw.ProgramWrapper(params, testmode=False)
                program.run_program()

    def vary_mai(self):
        for val in np.arange(self.mai_range[0], self.mai_range[1], self.mai_step):
            params = parameters(0.5, 125, Image.NEAREST, 10, 10, 110.7, 149.6, val, 'mm')
            program = pw.ProgramWrapper(params, testmode=False)
            program.run_program()
            
    def vary_whd_mai(self):
        for whd_val in np.arange(self.whd_range[0], self.whd_range[1], self.whd_step):
            for mai_val in np.arange(self.mai_range[0], self.mai_range[1], self.mai_step):
                params = parameters(0.5, 125, Image.NEAREST, whd_val, whd_val, 110.7, 149.6, mai_val, 'mm')
                program = pw.ProgramWrapper(params, testmode=False)
                program.run_program()

    def vary_whd_rf(self):
        for whd_val in np.arange(self.whd_range[0], self.whd_range[1], self.whd_step):
            for r_filter in np.arange(self.rf_num):
                params = parameters(0.5, 125, r_filter, whd_val, whd_val, 110.7, 149.6, 5, 'mm')
                program = pw.ProgramWrapper(params, testmode=False)
                program.run_program()

                

"""
EXECUTION
"""        
# Create VaryParameters instance.
vp = VaryParameters(whd_range, whd_step, mps_range, mps_step, mai_range, mai_step, rf_num)
        
# Grab the command.
try:
    command = sys.argv[1]
    print "command entered: ", command
except IndexError:
    print "Command/parameter type not provided."
    command = 'null'

# Function to execute command.
def executeCommand(parameter_type):
    if parameter_type == 'vary_whd':
        vp.width_height_divisors()
    elif parameter_type == 'vary_mps':
        vp.mid_perecent_save()
    elif parameter_type == 'vary_whd_mps':
        vp.vary_whd_mps()
    elif parameter_type == 'vary_mai':
        vp.vary_mai()
    elif parameter_type == 'vary_whd_mai':
        vp.vary_whd_mai()
    elif parameter_type == 'vary_whd_rf':
        vp.vary_whd_rf()
    else:
        print "Invalid vary command."

# Execute the command.
if command != 'null':
    executeCommand(command)
