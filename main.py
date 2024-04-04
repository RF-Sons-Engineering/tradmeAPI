from getCarDataframe import getListings
import json

# make = 'audi'
# model = 'a5'

# df = getListings(make, model)

# print(df.shape)


global makes_models

# Path to your JSON file
file_path = 'makes_models.json'

# Open the file and load the JSON data
with open(file_path, 'r') as file:
    makes_models = json.load(file)

def display_makes():

    print(list(makes_models.keys()))

display_makes()