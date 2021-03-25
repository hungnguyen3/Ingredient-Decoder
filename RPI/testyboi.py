import multiprocessing as mp
import time
import random
import PIL
from PIL import Image
import os

imageAltBit = 0

img1 = "/images/sushi.jpg"
img2 = "/images/chip.jpg"
img = img1
workingDir = os.path.dirname(os.path.abspath(__file__))


def produceImage(q):
    global img
    global imageAltBit
    q.put(imageAltBit)
    while True:
        time.sleep(random.randint(5, 15))
        print("new image")
        dummy = Image.open(workingDir + img)
        dummy = dummy.save(workingDir + "/images/testyboi.jpg")
        imageAltBit -= 1
        imageAltBit = (imageAltBit + 1) % 2 + 1
        q.put(imageAltBit)
        if img == "/images/sushi.jpg":
            img = "/images/chip.jpg"
        elif img == "/images/chip.jpg":
            img = "/images/sushi.jpg"
