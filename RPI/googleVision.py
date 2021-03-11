#GOOGLE VISION
import os
import base64
import requests
import json

#current working directory
workingDir = os.path.dirname(os.path.abspath(__file__))

#function convert images into base64 and create req body for API call
def prepareRequest(imgpath, type, max_results):
    req = None
    with open(imgpath, 'rb') as f_img:
        b64 = base64.b64encode(f_img.read()).decode()
        req = {
            'image': {
                'content': b64
            },
            'features': [{
                'type': type,
                'maxResults': max_results
            }]
        }
    return json.dumps({"requests": req}).encode()

#google cloud vision OCR API call
def requestOCR(url, key, imgpath):
    imgdata = prepareRequest(imgpath, 'TEXT_DETECTION', 1)
    response = requests.post(url,
                           data = imgdata,
                           params = {'key': key},
                           headers = {'Content-Type': 'application/json'})
    return response

def requestRecognition(url, key, imgpath):
    imgdata = prepareRequest(imgpath, 'LABEL_DETECTION', 5)
    response = requests.post(url,
                           data = imgdata,
                           params = {'key': key},
                           headers = {'Content-Type': 'application/json'})
    print("hello from requestRecognition")
    return response

def retrieveText(response):
    return response.json()["responses"][0]["textAnnotations"][0]["description"].lower()

def getMatchingArr(fullText, plist):
    matchingArr = []
    for element in plist:
        if element.lower() in fullText:
            matchingArr.append(element)
    return matchingArr
# convert image only
imgpath = workingDir + "/images/download.jpg"
imgtest = prepareRequest(imgpath, 'TEXT_DETECTION', 1)
#print(imgtest)

# make the request here
with open(workingDir + '/env.json') as f:
    data = json.load(f)

key = data["api_key"]
imgpath = workingDir + "/images/download.jpg"
visionURL = 'https://vision.googleapis.com/v1/images:annotate'

result = requestOCR(visionURL, key, imgpath)
text = retrieveText(result)
print(text)

matchingArr = getMatchingArr(text, ["VeGetAble Oil", "SALT", "Joe", "mama"])
print(matchingArr)
#print(result.json())

#result = requestRecognition(visionURL, key, imgpath)
#print(result.json())

