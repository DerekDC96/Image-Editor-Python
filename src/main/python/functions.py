
from sys import getsizeof
from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage

import numpy as np

# QImage(4) -> #D numpy.array of RGBA values ()
def imageToArray(self, img):
    img = img.convertToFormat(4)
    width = img.width()
    height = img.height()
    ptr = img.bits()
    ptr.setsize(img.byteCount())
    # copy the data into array (height width depth)
    arr = np.array(ptr).reshape(height, width, 4) 
    
    whydoesqimageusebgra = np.empty(arr.shape, dtype=np.uint8)
    whydoesqimageusebgra[..., 0] = arr[..., 2]
    whydoesqimageusebgra[..., 1] = arr[..., 1]
    whydoesqimageusebgra[..., 2] = arr[..., 0]
    whydoesqimageusebgra[..., 3] = 255
    
    return whydoesqimageusebgra

def arrayToImage(self, arr):
    height, width, channel = arr.shape
    bytesPerLine = 4 * width
    qimg = QImage(arr.data, width, height, bytesPerLine, QImage.Format_RGB32)
    return qimg


## numpy Array -> numpy Array
def blurFunction1(self, img):
    ## numpy array format: rows columns, color
    shape = np.array(img.shape)
    sAreaTable = np.empty(shape)  
    for i, row in enumerate(img):
        for j, pix in enumerate(row):
            for k, color in enumerate(pix):
                if i == 0 and j == 0:
                    sAreaTable[i][j][k] = int(color)
                elif i == 0:
                    sAreaTable[i][j][k] = int(color + sAreaTable[0][j - 1][k]) 
                elif j == 0:
                    sAreaTable[i][j][k] = int(color + sAreaTable[i-1][0][k])  
                else:
                    ## color needs to be constant - we don't want to blend colors
                    sAreaTable[i][j][k] = (color + sAreaTable[i-1][j][k] + sAreaTable[i][j - 1][k] - sAreaTable[i - 1][j - 1][k])
    

    blurredImage = np.empty(shape)
    for i, row in enumerate(sAreaTable):
        for k, pix in enumerate(row):
            for k, color in enumerate(pix):
                ## https://www.researchgate.net/figure/Box-filter-calculation-using-the-integral-image-the-shaded-area-indicates-the-filter-to_fig5_281771408
                ## edge cases, do nothing
                if i == 0 or j == 0 or i == sAreaTable.shape[0] - 1 or j == sAreaTable.shape[1] - 1:
                    blurredImage[i][j][k] = int(color)
                    
                else:
                    
                    blurredImage[i][j][k] = int((sAreaTable[i+1][j+1][k] + sAreaTable[i-2][j-2][k] - sAreaTable[i+1][j-2][k] - sAreaTable[i-2][j+1][k])/9)
    return blurredImage

def blurFunction(self, img):
    
    ## numpy array format: rows columns, color
    shape = np.array(img.shape)
    blurredImage = np.empty(shape)  
    for i, row in enumerate(img):
        for j, pix in enumerate(row):
            for k, color in enumerate(pix):
                if i == 0 or j == 0 or i == img.shape[0] - 1 or j == img.shape[1] - 1:
                    blurredImage[i][j][k] = img[i][j][k]
                    
                else:
                    blurredImage[i][j][k] = int((int(img[i-1][j-1][k]) + int(img[i-1][j][k]) + int(img[i-1][j+1][k]) +
                                                 int(img[i][j-1][k])   + int(img[i][j][k])   + int(img[i][j+1][k])   +
                                                 int(img[i+1][j-1][k]) + int(img[i+1][j][k]) + int(img[i+1][j+1][k])  /9))
                    

    return blurredImage

# numpy array -> numpy array
def grayscaleFunction(self, img):
    shape = np.array(img.shape)
    for i, row in enumerate(img):
        for j, pix in enumerate(row):
            ## compute linear transform of RGB values
            c_linear = (0.2126 * pix[0]/255.0) + (0.7152 * pix[1]/255.0) + (0.0722 * pix[2]/255.0)
            c_srgb = 1
            ## non-linear gamma correction
            if c_linear <= 0.0031308:
                c_srgb = c_linear * 12.92
            else:
                c_srgb = 1.055 * (c_linear**(1/2.4)) - 0.055
            pix[0] = c_srgb * 255    
            pix[1] = c_srgb * 255
            pix[2] = c_srgb * 255

        self.progress.emit(((i*100)-1)/shape[0])
    return img

def redtintFunction(self, img):
    shape = np.array(img.shape)
    print(img)
    for i, row in enumerate(img):
        for j, pix in enumerate(row):
            pix[0] = int(pix[0] * 1.25)
            if pix[0]>255:
                print("overflow?")
                pix[0] = 255    
            pix[1] = int(pix[1] * 0.75)
            pix[2] = int(pix[2] * 0.75)

        self.progress.emit(((i*100)-1)/shape[0])
    print(img[1])
    return img





                

