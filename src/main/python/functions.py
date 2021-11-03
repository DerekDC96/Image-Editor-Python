from PyQt5.QtGui import QPixmap, QImage
import numpy as np

# QImage(5) -> #D numpy.array of RGBA values ()
def imageToArray(img):
    width = img.width()
    height = img.height()
    ptr = img.bits()
    ptr.setsize(img.byteCount())
    # copy the data into array (height width depth)
    arr = np.array(ptr).reshape(height, width, 4) 
    return arr

def arrayToImage(arr):
    h, w, d = arr.shape
    qimg = QImage(arr, h, w, d, QImage.Format_RGB32)
    return qimg

## numpy array -> QImage
#def arrayToImage(arr):

## QImage -> QImage
def blurFunction(img):
    raw = imageToArray(img)
    ## numpy array format: rows columns, color
    ## summed-area table is the sum of all the pixels above and to the left of (x, y), inclusive
    shape = np.array(raw.shape)
    ## initialize summed area table
    sAreaTable = np.empty(shape)  
    for i, row in enumerate(raw):
        for j, pix in enumerate(row):
            for k, color in enumerate(pix):
                if i == 0 and j == 0:
                    sAreaTable[i][j][k] = int(color)
                elif i == 0:
                    sAreaTable[i][j][k] = int(color + sAreaTable[0][j - 1][k]) 
                elif j == 0:
                    sAreaTable[i][j][k] = int(color + sAreaTable[0][j][k - 1])  
                else:
                    ## color needs to be constant - we don't want to blend colors
                    sAreaTable[i][j][k] = int(color + sAreaTable[i - 1][j][k] + sAreaTable[i][j - 1][k] - sAreaTable[i - 1][j - 1][k])

    # blur the sAT
    blurredImage = np.empty(shape)
    for i, row in enumerate(sAreaTable):
        for k, pix in enumerate(row):
            for k, color in enumerate(pix):
                ## https://www.researchgate.net/figure/Box-filter-calculation-using-the-integral-image-the-shaded-area-indicates-the-filter-to_fig5_281771408
                
                ## edge cases, do nothing
                if i == 0 or j == 0 or i == blurredImage.shape[0] - 1 or j == blurredImage.shape[1] - 1:
                    blurredImage[i][j][k] = int(color)
                else:
                    blurredImage[i][j][k] = round(sAreaTable[i+1][j+1][k] + sAreaTable[i-2][j-2][k] - sAreaTable[i+1][j-2][k] - sAreaTable[i-2][j+1][k]) /9
    img = arrayToImage(blurredImage)
    return img

# QImage -> QImage

