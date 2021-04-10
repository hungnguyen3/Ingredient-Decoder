from PIL import Image
import os
import math
workingDir = os.path.dirname(os.path.abspath(__file__))

# this function take in an image and resize the image to be smaller than 400x400
# this helps putting the image onto the touchscreen app
def resizeImage(relative_path):
    try:
        readImg = Image.open(workingDir + relative_path)
    except OSError:
        readImg = Image.open(workingDir + "/images/Error.jpg")
        print(workingDir + relative_path)
        print('cannot open')
    width = readImg.width
    height = readImg.height
    while height > 400 or width > 400:
        height = height * 0.9
        width = width * 0.9
    width = math.floor(width)
    height = math.floor(height)
    readImg = readImg.resize((width, height), Image.ANTIALIAS)
    return readImg

# function to delete a tkinter label
def refresh(label):
    label.destroy()