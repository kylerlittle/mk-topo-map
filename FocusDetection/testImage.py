# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 13:26:06 2017

@author: kylerlittle
"""

import PIL as pil
import numpy as np

testImage = pil.Image.open("test_image.jpg");

pixels = np.asarray(testImage.convert('L'))
print pixels

print len(pixels[1])

#testImage.show()
