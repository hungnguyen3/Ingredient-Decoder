# GOOGLE VISION
import os
import base64
import requests
import json

# current working directory
workingDir = os.path.dirname(os.path.abspath(__file__))

# url of google vision API
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


# google cloud vision OCR(TEXT_DECTECTION) API call
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

# google cloud vision OBJECT_LOCALIZATION Recognition API call
def requestRecognition(img_path):
    retArray = []
    img_data = prepareRequest(img_path, 'OBJECT_LOCALIZATION', 10)
    result = requests.post(url,
                           data=img_data,
                           params={'key': key},
                           headers={'Content-Type': 'application/json'})
                           
    item = result.json()['responses'][0]['localizedObjectAnnotations']
    for i in item:
        print(i['name'])
        if i['score'] > minScore:
            retArray.append(i['name'])

    return retArray

# get an overlapping array of all the similar items between full_text and plist
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


# this is a small test to see if above functions works fine
def TestGround():
    img_path = "/images/appana.jpg"
    result = requestRecognition(img_path)

    print(result)
    matchingArr = getMatchingArr(result, ["VeGetAble Oil", "SALT", "Joe", "mama"])
    print(matchingArr)

# TestGround()