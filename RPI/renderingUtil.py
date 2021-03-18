from PIL import Image
import os
import math
workingDir = os.path.dirname(os.path.abspath(__file__))

def resizeImage(relative_path):
    readImg = Image.open(workingDir + relative_path)
    width = readImg.width
    height = readImg.height
    while height > 500 or width > 500:
        height = height * 0.9
        width = width * 0.9
    width = math.floor(width)
    height = math.floor(height)
    readImg = readImg.resize((width, height), Image.ANTIALIAS)
    return readImg


def refresh(label):
    label.destroy()
