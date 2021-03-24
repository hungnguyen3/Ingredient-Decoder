import cv2
import numpy as np
import os

path = os.path.dirname(os.path.abspath(__file__))
imgPath = os.path.dirname(path) + "/images"

def cropImage(imageName, xMin, xMax, yMin, yMax):
    img = cv2.imread(imgPath + imageName)
    print(img)
    crop = img[yMin:yMax, xMin:xMax]
    filename = imgPath + '/download.jpg'
    cv2.imwrite(filename, crop)
    print("image cropped")

#cropImage('/small.jpg', 8,141,31,85)