import requests
import list

pListUrl = "http://52.138.39.36:3000/plist"
customIngredientsUrl = "http://52.138.39.36:3000/search_byname"


def Get_Personal_List(username):
    PARAMS = {'username': username}
    response = requests.post(url=pListUrl, json=PARAMS)
    resJson = response.json()
    userList = []

    for element in resJson['message']:
        userList.append(element["p"])

    return userList


def Get_Custom_Ingredients(item_list):
    ingredients = ""
    missCounter = 0
    errorOne = {'message': 'err plist'}
    errorTwo = {'message': None}
    for i in item_list:
        # db.collection("store").find({$or:[{"owner": req.body.to_search},{"item_name":req.body.to_search}]}).toArray(function(err,data){
        PARAMS = {'to_search': i}
        response = requests.post(url=customIngredientsUrl, json=PARAMS)
        resJson = response.json()
        for field in resJson['message']:
            if field != errorOne and field != errorTwo:
                ingredients += " " + field['item_list']
            else:
                missCounter += 1

    # for element in resJson['message']:
    #     userList.append(element["p"])
    print(item_list)
    print(missCounter)
    print(len(item_list))
    if missCounter == len(item_list):
        return "notRecognition"
    print("OWO "+ ingredients)
    return ingredients

def Get_Harmful_List():
    return list.list


def TestyBoi():
    # BogusList = Get_Custom_Ingredients(['Newspaper', 'Plant', 'Font', 'Material property'])
    print(Get_Harmful_List())


# TestyBoi()
