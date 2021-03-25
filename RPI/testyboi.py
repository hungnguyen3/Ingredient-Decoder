import multiprocessing as mp
import time
import random
import PIL
from PIL import Image
import os


img1 = "/images/download.jpg"
img2 = "/images/download.jpg"
img = img1
workingDir = os.path.dirname(os.path.abspath(__file__))


def produceImage(outputQ, ackQ):

    global img
    takeNew = False
    while True:
        # time between images
        time.sleep(random.randint(1, 5))

        if not ackQ.empty():
            # image process time
            takeNew = ackQ.get()
        if takeNew:
            time.sleep(random.randint(2, 6))
            print("new image")
            dummy = Image.open(workingDir + img)
            dummy = dummy.save(workingDir + "/images/testyboi.jpg")
            outputQ.put(True)
            if img == img1:
                img = img2
            elif img == img2:
                img = img1
            takeNew = False
