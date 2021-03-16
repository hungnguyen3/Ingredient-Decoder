import time
import random


def takeImage(img):
    if random.randint(0, 99) < 10:
        return True, (img), True
    return False, "false", False