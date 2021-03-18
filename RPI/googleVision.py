# GOOGLE VISION
import os
import base64
import requests
import json
import debugUtil

# current working directory
workingDir = os.path.dirname(os.path.abspath(__file__))
url = 'https://vision.googleapis.com/v1/images:annotate'
with open(workingDir + '/env.json') as f:
    data = json.load(f)

key = data["api_key"]
minScore = 0.8


# function convert images into base64 and create req body for API call
def prepareRequest(img_path, recognition_type, max_results):
    req = None
    with open(workingDir + img_path, 'rb') as f_img:
        b64 = base64.b64encode(f_img.read()).decode()
        req = {
            'image': {
                'content': b64
            },
            'features': [{
                'type': recognition_type,
                'maxResults': max_results
            }]
        }
    return json.dumps({"requests": req}).encode()


# google cloud vision OCR API call
def requestOCR(img_path):
    img_data = prepareRequest(img_path, 'TEXT_DETECTION', 1)
    response = requests.post(url,
                             data=img_data,
                             params={'key': key},
                             headers={'Content-Type': 'application/json'})
    try:
        response = response.json()["responses"][0]["textAnnotations"][0]["description"].lower()
        return response
    except KeyError:
        return "notOCR"




def requestRecognition(img_path):
    img_data = prepareRequest(img_path, 'LABEL_DETECTION', 10)
    result = requests.post(url,
                           data=img_data,
                           params={'key': key},
                           headers={'Content-Type': 'application/json'})
    result = [item.get('description')
              for item in result.json()["responses"][0]["labelAnnotations"]
              if item["score"] > minScore]

    return result


def getMatchingArr(full_text, plist):
    matchingArr = []
    if full_text == "notOCR":
        return "notOCR"
    if full_text == "notRecognition":
        return "notRecognition"
    for element in plist:
        if element.lower() in full_text and (element.lower() not in matchingArr):
            matchingArr.append(element.lower())
    return matchingArr


# make the request here

def TestGround():
    img_path = "/images/download.jpg"
    result = requestRecognition(img_path)

    print(result)
    # matchingArr = getMatchingArr(text, ["VeGetAble Oil", "SALT", "Joe", "mama"])
    # print(matchingArr)
    #
    # result = requestRecognition(visionURL, key, imgpath)
    # print(result.text)
    # li = [item.get('description') for item in result.json()["responses"][0]["labelAnnotations"]]
    # print(li)


# TestGround()
