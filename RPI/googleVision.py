#GOOGLE VISION
import os
import base64
import requests
import json

#current working directory
workingDir = os.path.dirname(os.path.abspath(__file__))

#function convert images into base64 and create req body for API call
def makeImageData(imgpath):
    req = None
    with open(imgpath, 'rb') as f_img:
        b64 = base64.b64encode(f_img.read()).decode()
        req = {
            'image': {
                'content': b64
            },
            'features': [{
                'type': 'DOCUMENT_TEXT_DETECTION',
                'maxResults': 1
            }]
        }
    return json.dumps({"requests": req}).encode()

#google cloud vision ORC API call
def requestOCR(url, key, imgpath):
    imgdata = makeImageData(imgpath)
    response = requests.post(url,
                           data = imgdata,
                           params = {'key': key},
                           headers = {'Content-Type': 'application/json'})
    return response

# def detect_labels(path):
#     """Detects labels in the file."""
#     from google.cloud import vision
#     import io
#     client = vision.ImageAnnotatorClient()
#
#     with io.open(path, 'rb') as image_file:
#         content = image_file.read()
#
#     image = vision.Image(content=content)
#
#     response = client.label_detection(image=image)
#     labels = response.label_annotations
#     print('Labels:')
#
#     for label in labels:
#         print(label.description)
#
#     if response.error.message:
#         raise Exception(
#             '{}\nFor more info on error messages, check: '
#             'https://cloud.google.com/apis/design/errors'.format(
#                 response.error.message))

# convert image only
#imgpath = workingDir + "/images/download.jpg"
#imgtest = makeImageData(imgpath)
#print(imgtest)

# make the request here
with open(workingDir + '/env.json') as f:
    data = json.load(f)

key = data["api_key"]
imgpath = workingDir + "/images/download.jpg"
visionURL = 'https://vision.googleapis.com/v1/images:annotate'

result = requestOCR(visionURL, key, imgpath)
print(result.json())
#
# objectPath = "images/sushi.bmp"
# result = detect_labels()