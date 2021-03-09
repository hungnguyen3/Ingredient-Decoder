# Import the base64 encoding library.
import base64
import os

workingDir = os.path.dirname(os.path.abspath(__file__))

# Pass the image data to an encoding function.
def encode_image(image):
  image_content = image.read()
  return base64.b64encode(image_content)

imgpath = workingDir + "/images/sushi.bmp"
with open(imgpath, 'rb') as f_img:
    result = encode_image(f_img)

print(result)