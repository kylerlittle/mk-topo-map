# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 12:25:46 2017

@author: kylerlittle
"""

#Libraries Included
from Laplacian_Variance import variance_of_laplacian
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from parameters import parameters

def plot_threeDmodel(model, dimension_units, modelDir, p, testModeOn):
    print "[x] Graphing 3D Model"
    # Set up plot.    
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    
    # Set up grid and test data
    (Width,Height) = model.shape
    x = np.arange(Height)    # x actually corresponds with 'y' axis
    y = np.arange(Width)     # y actually corresponds with 'x' axis
    
    X, Y = np.meshgrid(x, y)  # `plot_surface` expects `x` and `y` data to be 2D
    # 'meshgrid' converts coordinates to two separate 2D arrays
    
    Z = model.reshape((Width,Height))  #flip plot upside down
    surf = ax.plot_surface(X, Y, Z, cmap=cm.summer, linewidth=0, antialiased=False)
    
    # Customize the z axis.
    ax.zaxis.set_major_locator(LinearLocator(10))    #evenly spaced ticks from min to max
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))    
    
    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)    
    
    # Label my axes
    plt.title('Topographical Map', fontsize=14, color='blue')
    ax.set_xlabel('Length (' + dimension_units + ')', fontsize=10, color='blue')
    ax.set_ylabel('Width (' + dimension_units + ')', fontsize=10, color='blue')
    ax.set_zlabel('Height (' + dimension_units + ')', fontsize=10, color='blue')
    
    # Set default viewing angle
    ax.view_init(elev=40, azim=-114)

    if testModeOn:   # Display figure rather than saving it.
        plt.show()
    else:          # Save fig with parameters in name & without surround whitespace
        """
        Naming standard: fig_middlePercentSavings(%)_cropThresholdLevel_resizingFilter_widthDivisor_heightDivisor_
                         startHeight_endHeight_maxAllowableIterations.png
        """
        nameOfFig = modelDir + "fig_" + "{0:.0f}mps".format(p.mps*100) + '_' + str(p.ctl) + "ctl" + '_' + str(p.rf) + "rf" + '_' + str(p.wd) + "wd" + '_' + str(p.hd) + "hd" + '_' + str(int(round(p.sh, 0))) + "sh" + '_' + str(int(round(p.eh, 0))) + "eh" + '_' + str(p.mai) + "mai" + ".png"
        fig.savefig(nameOfFig, bbox_inches='tight')
