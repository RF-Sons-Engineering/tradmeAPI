import requests
import json

def getMakes():

    url = "https://api.trademe.co.nz/v1/Categories/UsedCars.json"

    response = requests.request("GET", url)

    return response.json()

def getModels(category):

    url = f"https://api.trademe.co.nz/v1/Categories/{category}/Details.json"

    response = requests.request("GET", url)

    return response.json()


def get_make_and_models():

    makes_and_models = {}

    makes = getMakes()
    
    for make in makes['Subcategories']:
        name = make['Name']
        category_id = make['Number']
   
        model_list = []
        models = getModels(category_id)
        for model in models['Attributes'][0]['Options']:
            model_list.append(model['Value'])
        
        makes_and_models[name] = model_list
    

    return makes_and_models


# Example usage
# makes = getMakes()
# # print(json.dumps(response, indent=4))
# for make in makes['Subcategories']:
#     print(f'===== {make['Name']} =========')
#     category_id = make['Number']
#     models = getModels(category_id)
#     for model in models['Attributes'][0]['Options']:
#         print(model['Value'])

# makes_and_models = get_make_and_models()

# print(makes_and_models.keys())