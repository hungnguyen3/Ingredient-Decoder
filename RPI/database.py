import requests
import list

pListUrl = "http://52.138.39.36:3000/plist"
customIngredientsUrl = "http://52.138.39.36:3000/plist"


def Get_Personal_List(username):
    PARAMS = {'username': username}
    response = requests.post(url=pListUrl, json=PARAMS)
    resJson = response.json()
    userList = []

    print(resJson)
    for element in resJson['message']:
        userList.append(element["p"])

    return userList


def Get_Custom_Ingredients(item_list):
    ingredientsList = []
    for i in item_list:
        PARAMS = {'item': i}
        response = requests.post(url=customIngredientsUrl, json=PARAMS)
        resJson = response.json()
        errorOne = {'message': 'err plist'}
        errorTwo = {'message': None}
        if resJson != errorOne and resJson != errorTwo:
            ingredientsList += resJson
        print(resJson == errorTwo)

    # for element in resJson['message']:
    #     userList.append(element["p"])

    return ingredientsList

def Get_Harmful_List():
    return list.list


def TestyBoi():
    # BogusList = Get_Custom_Ingredients(['Newspaper', 'Plant', 'Font', 'Material property'])
    print(Get_Harmful_List())


# TestyBoi()
