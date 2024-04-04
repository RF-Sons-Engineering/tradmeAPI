import requests
from constructURL import construct_url
from refreshToken import refreshToken
import json


def getTrademePrediction(number_plate, odometer, token):

    baseurl = f'https://api.trademe.co.nz/v1/motors/valuation/car/{number_plate}/{odometer}.json'

    headers = {
    'Authorization': f'Bearer {token}'
    }

    response = requests.request("GET", baseurl, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return response.text


# # Example usage
# number_plate = 'PET520'
# odometer = '71900'

# token = refreshToken()

# data = getTrademePrediction(number_plate, odometer, token)

# print(json.dumps(data, indent=4))
