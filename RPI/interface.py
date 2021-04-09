import time
import random

# used for testing
# would create image in directory randomly, simulating async camera
# return an image randomly
def takeImage():
    if random.randint(0, 99) < 50:
        return True, "/images/banapple.jpg", True
    return False, "false", False