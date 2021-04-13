from unittest import TestCase
import renderingUtil as dut
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


workingDir = dut.workingDir

#test if the image resize works
class Test(TestCase):
    def test_resize_image(self):
        for filename in os.listdir(workingDir + "/images"):
            img = dut.resizeImage("/images/" + filename)
            imgplot = plt.imshow(img)
            plt.show()
            
            # test if the image is smaller than expected size
            assert img.width < 500 and img.height < 500
            img.close()
