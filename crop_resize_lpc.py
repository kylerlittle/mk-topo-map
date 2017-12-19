




"""
Shoving everything into one function right now. Will fix later.
"""


def crop_resize_lpc(middlePercentSaving, cropThresholdLevel, heightDivisor, widthDivisor):

    def cropPhotos(self, middlePercentSaving, cropThresholdLevel):
                imageList = os.listdir(rawImagesDir)
                        if not imageList:
                                        print "Please populate 'rawImages/' with images."
                        else:
                                        print "[x] Initiating image cropping"
                                                    counter = 1;
                                                                for imStr in imageList:
                                                                                    trm.trim(rawImagesDir + imStr, croppedImagesDir + "croppedIm" + str(counter) + ".jpg", middlePercentSaving, cropThresholdLevel, counter)
                                                                                                    counter += 1



        self.smallestImage = smallestImage(croppedImagesDir)
                imageList = os.listdir(croppedImagesDir)
                        if not imageList:
                                        print "Try running 'make crop' first."
                        else:
                                        counter = 1   # utilize counter for appropriate file naming
                                                    print "[x] Resizing all images to: ", self.smallestImage
                                                                for imStr in imageList:
                                                                                    im = Image.open(croppedImagesDir + imStr)
                                                                                                    print "\t[", counter, "] ", im.size[0], ",", im.size[1], "resized to",
                                                                                                                    resizedIm = im.resize(self.smallestImage, resample=Image.LANCZOS)    # resize using LANCZOS filtering
                                                                                                                                    print resizedIm.size[0], ",", resizedIm.size[1]
                                                                                                                                                    resizedIm.save(resizedImagesDir + "readyToAnalyze" + str(counter) + ".jpg")   # save resized im to correct dir
                                                                                                                                                                    im.close()
                                                                                                                                                                                    counter += 1




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

imageList = os.listdir(resizedImagesDir)
        if not imageList:
                        print "Try running 'make resize' first."
        else:
                        print "[x] Initiating 'variance_of_laplacian' method on resized images"
                                    counter = 1   # Counter included for console output
                                                for imStr in imageList:
                                                                    varianceMatrix = variance_of_laplacian(resizedImagesDir + imStr, heightDivisor, widthDivisor, counter)
                                                                                    counter += 1
                                                                                                    self.laplacianImageStack.append(varianceMatrix) # For each matrix produced from a single image, append to internal list
                                                                                                                with open(internalList, 'wb') as f:
                                                                                                                                    pickle.dump(self.laplacianImageStack, f, protocol=pickle.HIGHEST_PROTOCOL)
