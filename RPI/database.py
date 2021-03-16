import requests
import list

pListUrl = "http://52.138.39.36:3000/plist"
customIngredientsUrl = "http://52.138.39.36:3000/plist"


def Get_Personal_List(username):
    PARAMS = {'username': username}
    response = requests.post(url=pListUrl, json=PARAMS)
    resJson = response.json()
    userList = []

    for element in resJson['message']:
        userList.append(element["p"])

    return userList


def Get_Custom_Ingredients(item_list):
    ingredientsList = []
    missCounter = 0
    errorOne = {'message': 'err plist'}
    errorTwo = {'message': None}
    for i in item_list:
        PARAMS = {'item': i}
        response = requests.post(url=customIngredientsUrl, json=PARAMS)
        resJson = response.json()
        if resJson != errorOne and resJson != errorTwo:
            ingredientsList += resJson
        else:
            missCounter += 1

    # for element in resJson['message']:
    #     userList.append(element["p"])
    print(item_list)
    print(missCounter)
    print(len(item_list))
    if missCounter == len(item_list):
        return "notRecognition"
    return ingredientsList

def Get_Harmful_List():
    return list.list


def TestyBoi():
    # BogusList = Get_Custom_Ingredients(['Newspaper', 'Plant', 'Font', 'Material property'])
    print(Get_Harmful_List())


# TestyBoi()
