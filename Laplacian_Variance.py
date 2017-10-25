# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 14:39:17 2017

@author: kylerlittle
"""
"""

Purpose: Compute the Variance of the Laplacian of an image.

Key terms:

    Image Convolution: In image processing, a kernel (small matrix) is used
    for blurring, sharpening, edge detecting, etc. It is accomplished by
    convolving an image and the kernel.
        Convolution is a nontraditional way of multiplying two matrices.
        
    Matrix of Image:
    The matrix of an image arises from the fact that natural images
    are stored as "bitmap" images. A bitmap image take the form of an array, 
    where the value of each element, called a pixel picture element, 
    corresponds to the color of that portion of the image. Each horizontal 
    line in the image is called a scan line.

"""

#Libraries Included
import pylab as pl   #numpy & plotting capabilities
import PIL as pil    #imaging capabilities
from scipy import signal   #convolving operation, optimized for large matrices
from PIL import Image  #size of 'image' operation


"""
Function: variance_of_laplacian
Background: The Laplacian operator measures the 2nd derivate of the image.
             Since the image's entries are (of course) not functions, the
             Laplacian operator is performed by convolving the image with
             a Laplacian 'kernel.' When I calculate the variance of the 
             result, I can find meaning in that value. A high variance
             indicates a wide spread of responses, both edge-like and
             non-edge like. These are qualities of an in-focus image.
             A low variance indicates there are few edges, indicating
             blurriness.
Description: This function divides an image into (m/10)*(n/10) submatrices,
             where m and n represent the size of the image in pixels. Each
             submatrix is convolved with the Laplacian Kernel. Then, the
             variance of the result is computed and stored into a matrix
             1/100th the size of the original image (at its relative location).
             
             
             
Input Parameters: File_Name (of image)
Preconditions: rWidth and rHeight must be divisible by 10
Returns: Variance of Laplacian Matrix (size: m/10 x n/10) where mxn are 
         dimensions of image in pixels.
"""
def variance_of_laplacian(filename):
    # Variables
    image = Image.open(filename)     # open file
    (rWidth, rHeight) = image.size     # returns width, height or x, y or cols, rows
    image.close();      # close file
    totalImageRows = pl.arange(rHeight / 10)   
    totalImageColumns = pl.arange(rWidth / 10)
    numRows_MiniMatrix = numCols_MiniMatrix = pl.arange(10)
    miniMatrix = pl.zeros((10,10)) # 10x10 Matrix to copy elements to    
    varianceMatrix = pl.zeros((rHeight / 10, rWidth / 10))
    Laplacian_Kernel = (pl.array([[0.,-1.,0.],[-1.,4.,-1.],[0.,-1.,0.]])) * (1./60)
    
    # 1. Convert image to matrix.
    toBeConverted = pil.Image.open(filename)
    toBeConverted = toBeConverted.resize([(rWidth / 10) * 10,(rHeight / 10) * 10])  # resize (columns, width)
    # truncating the width and height so that they're divisible by 10
    imageMatrix = pl.asarray(toBeConverted.convert('L')) # convert image to greyscale; return matrix
    toBeConverted.close();  # close file
    
    # 2. Split Image into sub-matrices, each of size 10x10. For each 
    #    10x10 sub-matrix, convolve with the kernel. Calculate the variance
    #    of this convolution. Place variance in a 200x400 matrix.    

    for subset_of_rows in totalImageRows:  # TOTAL Image Matrix
        for subset_of_columns in totalImageColumns:
            image_row = subset_of_rows * 10 # keeps track of larger matrix's row index to copy from 
            image_col = subset_of_columns * 10 # keeps track of larger matrix's dolumn index to copy from
            for row in numRows_MiniMatrix:
                for col in numCols_MiniMatrix:
                    miniMatrix[row][col] = imageMatrix[image_row + row][image_col + col]
            # 3. Convolve part of the image with the Laplacian kernel
            Convolve = signal.fftconvolve(miniMatrix, Laplacian_Kernel, mode='full')
            # 4. Compute the variance of the convolution.
            Variance = pl.var(Convolve)
            # 5. Store variance in entry of varianceMatrix
            varianceMatrix[subset_of_rows][subset_of_columns] = Variance
   # 6. return the varianceMatrix
    return varianceMatrix


#TESTING
#test = variance_of_laplacian("test_image_2.jpg")
#pl.savetxt('test_file', test, delimiter=',')
    
    
"""
Testing:
1. Set the focal length to a specific height (distance to platform).
2. Take image. This is the "base case." Height = distance to focal plane.
   Should be a high average variance.
3. Raise the platform by a known height. Take image.
4. Record average of all entries of varianceMatrix.
5. Repeat until desired range of heights is recorded.
6. Graph distance vs. average variance. Hopefully it's linear.

Results:
If it is linear, then I can correspond my arbitrary variance values
to physical real-world values! Then my 3D_plotting function can be modified
so that the z-axis essentially represents the 'displacement' from the focal
plane. This is useful because it will allow me to recover the depth of an
object by simply taking an image overtop.
If it is not linear, then I can still do what I said above... but I better
not extrapolate. I won't be extrapolating anyways, but a polynomial-like
functions might be difficult to deal with. Nonetheless, I will not use the
function fitted to the graph of 'Distance v. Average Variance' to extrapolate.
I will only use predicted values within the range of my data set.

Comments:
I will need to differentiate between color & edge detection. I don't want
my function mistakenly getting a high variance because there are many
different colors present in the image.
"""