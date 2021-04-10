import requests
import list

# urls to the backend server
pListUrl = "http://52.138.39.36:3000/plist"
customIngredientsUrl = "http://52.138.39.36:3000/search_byname"

# send a get request to the backend to get cutomer's personal list
def Get_Personal_List(username):
    PARAMS = {'username': username}
    response = requests.post(url=pListUrl, json=PARAMS)
    resJson = response.json()
    userList = []

    for element in resJson['message']:
        userList.append(element["p"])

    return userList

# get the ingredients of a store custom item
def Get_Custom_Ingredients(item_list):
    ingredients = []
    errorOne = {'message': 'err plist'}
    errorTwo = {'message': None}
    for i in item_list:
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

# get general harmful substances
def Get_Harmful_List():
    return list.list

# this is a small test for the functions above
def TestyBoi():
    # BogusList = Get_Custom_Ingredients(['Newspaper', 'Plant', 'Font', 'Material property'])
    print(Get_Harmful_List())

# TestyBoi()