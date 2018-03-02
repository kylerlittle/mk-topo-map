# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 12:25:46 2017

@author: kylerlittle
"""

#Libraries Included
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from scipy import interpolate
from parameters import parameters

def plot_three_d_model(model, dimension_units, modelDir, p, testModeOn):
    print "[x] Graphing 3D Model"

    """
    # CODE FOR WIRE_FRAME PLOT:
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')  #111 means 1x1 block of graphs and subplot 1
    (Width,Height) = model.shape
    x = np.arange(Width) 
    x = x[10:31:1]
    y = np.arange(Height)  
    Y, X = np.meshgrid(y, x)  # `plot_surface` expects `x` and `y` data to be 2D
    model = model[10:31:1][::]
    Z = model
    surf = ax.plot_wireframe(X, Y, Z, rstride=1, cstride=5)
    ax.zaxis.set_major_locator(LinearLocator(10))    #evenly spaced ticks from min to max
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))    
    plt.title('Topographical Map', fontsize=14, color='blue')
    ax.set_xlabel('Length (' + dimension_units + ')', fontsize=10, color='blue')
    ax.set_ylabel('Width (' + dimension_units + ')', fontsize=10, color='blue')
    ax.set_zlabel('Height (' + dimension_units + ')', fontsize=10, color='blue')
    ax.view_init(elev=40, azim=-114)
    plt.show()
    """
    # Set up surface_plot.    
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    
    # Set up grid and test data
    (Height,Width) = model.shape
    y = np.arange(Height)
    x = np.arange(Width)
    X, Y = np.meshgrid(x, y)  # `plot_surface` expects `x` and `y` data to be 2D
    # 'meshgrid' converts coordinates to two separate 2D arrays
    Z = model[:][:]
    
    #xnew, ynew = np.mgrid[-1:1:560j, -1:1:84j]
    #tck = interpolate.bisplrep(X, Y, Z, s=0)
    #znew = interpolate.bisplev(xnew[:,0], ynew[0,:], tck)
    surf = ax.plot_surface(X, Y, Z, cmap=cm.summer, rstride=1, cstride=1,linewidth=0, antialiased=False)
    
    # Customize the z axis.
    ax.zaxis.set_major_locator(LinearLocator(10))    #evenly spaced ticks from min to max
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    # Input matrix is rectangular, so set the aspect of the axis scaling to avoid a cubic plot
    #z_min = Z.min(); z_max = Z.max()
    # In the future, make this more reusable. For now, it's easiest to just do this manually.
    # max_val = max(len(x), len(y), abs(z_min - z_max))
    #ax.pbaspect = [1.5, 0.4, 0.4]
    #ax.auto_scale_xyz([0, max_val], [0, max_val], [z_min - 5, z_max + 5])
    
    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)
    
    # Label my axes
    plt.title('Topographical Map', fontsize=14, color='blue')
    ax.set_xlabel('Length (' + dimension_units + ')', fontsize=10, color='blue')
    ax.set_ylabel('Width (' + dimension_units + ')', fontsize=10, color='blue')
    ax.set_zlabel('Height (' + dimension_units + ')', fontsize=10, color='blue')
    
    # Set default viewing angle
    ax.view_init(elev=67, azim=-156)

    if testModeOn:   # Display figure rather than saving it.
        plt.show()
    else:          # Save fig with parameters in name & without surround whitespace
        """
        Naming standard: fig_middlePercentSavings(%)_cropThresholdLevel_resizingFilter_widthDivisor_heightDivisor_
                         startHeight_endHeight_maxAllowableIterations.png
        """
        nameOfFig = modelDir + "third-run/" + "fig_" + "{0:.0f}mps".format(p.mps*100) + '_' + str(p.ctl) + "ctl" + '_' + str(p.rf) + "rf" + '_' + str(p.wd) + "wd" + '_' + str(p.hd) + "hd" + '_' + str(int(round(p.sh, 0))) + "sh" + '_' + str(int(round(p.eh, 0))) + "eh" + '_' + str(p.mai) + "mai" + ".png"
        fig.savefig(nameOfFig, bbox_inches='tight')
