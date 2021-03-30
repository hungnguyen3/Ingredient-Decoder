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
    ingredients = []
    errorOne = {'message': 'err plist'}
    errorTwo = {'message': None}
    for i in item_list:
        # db.collection("store").find({$or:[{"owner": req.body.to_search},{"item_name":req.body.to_search}]}).toArray(function(err,data){
        PARAMS = {'to_search': i}
        response = requests.post(url=customIngredientsUrl, json=PARAMS)
        resJson = response.json()
        if resJson['message'] == []:
            ingredients.append('0')
        for field in resJson['message']:
            if field != errorOne and field != errorTwo:
                ingredients.append(field['item_list'])

    print("ingredients array")
    print(ingredients)
    return ingredients

def Get_Harmful_List():
    return list.list


def TestyBoi():
    # BogusList = Get_Custom_Ingredients(['Newspaper', 'Plant', 'Font', 'Material property'])
    print(Get_Harmful_List())


# TestyBoi()