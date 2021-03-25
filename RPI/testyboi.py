import multiprocessing as mp
import time
import random
import PIL
from PIL import Image
import os

imageAltBit = 0

img1 = "/images/download.jpg"
img2 = "/images/download.jpg"
img = img1
workingDir = os.path.dirname(os.path.abspath(__file__))


def produceImage(q):
    global img
    global imageAltBit
    q.put(imageAltBit)
    while True:
        time.sleep(3)
        print("new image")
        dummy = Image.open(workingDir + img)
        dummy = dummy.save(workingDir + "/images/testyboi.jpg")
        imageAltBit -= 1
        imageAltBit = (imageAltBit + 1) % 2 + 1
        q.put(imageAltBit)
        #if img == "/images/download.jpg":
        #    img = "/images/chip.jpg"
        #elif img == "/images/chip.jpg":
        #    img = "/images/download.jpg"