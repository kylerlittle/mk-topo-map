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
Description: This function divides an image into (m/heightDivisor)*(n/widthDivisor) submatrices,
             where m and n represent the size of the image in pixels. Each
             submatrix is convolved with the Laplacian Kernel. Then, the
             variance of the result is computed and stored into a matrix
             1/(heightDivisor*widthDivisor)th the size of the original image (at its relative location).
Input Parameters: File_Name (of image), heightDivisor, widthDivisor
Returns: Variance of Laplacian Matrix (size: (rHeight / heightDivisor)
         x (rWidth / widthDivisor)) where mxn are dimensions of image in pixels.
"""
def variance_of_laplacian(filename, heightDivisor, widthDivisor, counter):
    # Variables
    image = Image.open(filename)     # open file
    (rWidth, rHeight) = image.size     # returns width, height or x, y or cols, rows
    image.close();      # close file
    totalImageRows = pl.arange(rHeight / heightDivisor)   
    totalImageColumns = pl.arange(rWidth / widthDivisor)
    numRows_MiniMatrix = pl.arange(heightDivisor)
    numCols_MiniMatrix = pl.arange(widthDivisor)
    miniMatrix = pl.zeros((heightDivisor,widthDivisor)) # heightDivisor x widthDivisor Matrix to copy elements to    
    varianceMatrix = pl.zeros((rHeight / heightDivisor, rWidth / widthDivisor))
    Laplacian_Kernel = (pl.array([[0.,-1.,0.],[-1.,4.,-1.],[0.,-1.,0.]])) * (1./60)
    
    # 1. Convert image to matrix.
    toBeConverted = pil.Image.open(filename)
    # resize (columns, width)
    toBeConverted = toBeConverted.resize([(rWidth / widthDivisor) * widthDivisor,(rHeight / heightDivisor) * heightDivisor], resample=Image.LANCZOS)    # resize using LANCZOS filtering
    # truncating the width and height so that they're divisible by heightDivisor & widthDivisor
    imageMatrix = pl.asarray(toBeConverted.convert('L')) # convert image to greyscale; return matrix
    toBeConverted.close();  # close file
    
    # 2. Split Image into sub-matrices, each of size heightDivisor x widthDivisor. For each 
    #    heightDivisor x widthDivisor sub-matrix, convolve with the kernel. Calculate the variance
    #    of this convolution. Place variance in a (rHeight / heightDivisor) x (rWidth / widthDivisor) matrix.    

    print "\t[", counter, "] Convolving subdivisions of image with Laplacian Kernel... Calculating Variance... ",
    for subset_of_rows in totalImageRows:  # TOTAL Image Matrix
        for subset_of_columns in totalImageColumns:
            image_row = subset_of_rows * heightDivisor # keeps track of larger matrix's row index to copy from 
            image_col = subset_of_columns * widthDivisor # keeps track of larger matrix's dolumn index to copy from
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
    print "Done."
    return varianceMatrix
