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

def plot_variance_image(varianceMatrix_):
    # Set up plot.    
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    
    # Set up grid and test data
    (Width,Height) = varianceMatrix_.shape
    x = np.arange(Height)    # x actually corresponds with 'y' axis
    y = np.arange(Width)     # y actually corresponds with 'x' axis
    
    X, Y = np.meshgrid(x, y)  # `plot_surface` expects `x` and `y` data to be 2D
    # 'meshgrid' converts coordinates to two separate 2D arrays
    
    Z = varianceMatrix_.reshape((Width,Height))  #flip plot upside down
    surf = ax.plot_surface(X, Y, Z, cmap=cm.YlOrRd, linewidth=0, antialiased=False)
    
    # Customize the z axis.
    ax.zaxis.set_major_locator(LinearLocator(10))    #evenly spaced ticks from min to max
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))    
    
    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)    
    
    # Label my axes
    plt.title('Edge Detection Plot', fontsize=14, color='blue')
    ax.set_xlabel('Vertical Direction (1.00E2 pixels)', fontsize=10, color='blue')
    ax.set_ylabel('Horizontal Direction (1.00E2 pixels)', fontsize=10, color='blue')
    ax.set_zlabel('Variance of Laplacian (arb. units)', fontsize=10, color='blue')
    
    # Set default viewing angle
    ax.view_init(elev=-120, azim=-135)
    
    plt.show()
    
    
# TESTING

test = variance_of_laplacian("test_image.jpg")
plot_variance_image(test)
    
#test2 = variance_of_laplacian("test_image_fiber.jpg")
#plot_variance_image(test2)    

#test3 = variance_of_laplacian("focus.jpg")
#plot_variance_image(test3)

test4 = variance_of_laplacian("coug.jpg")
plot_variance_image(test4)