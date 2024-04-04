import json
from getMakesModels import get_make_and_models

# Sample dictionary
data = get_make_and_models()

# Specify the file name
file_name = 'makes_models.json'

# Write dictionary to a file
with open(file_name, 'w') as file:
    json.dump(data, file, indent=4)