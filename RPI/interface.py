import time
import random


def takeImage(img):
    if random.randint(0, 99) < 10:
        return True, (img + "/images/download.jpg")
    return False, "false"