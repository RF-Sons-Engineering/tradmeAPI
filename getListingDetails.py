import requests

def getListingDetails(listingId, token):

    headers = {
    'Authorization': f'Bearer {token}'
    }

    url = f'https://api.trademe.co.nz/v1/Listings/{listingId}.json?increment_view_count=false'

    response = requests.request("GET", url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return response.text


# # Example usage
from refreshToken import refreshToken
import json


# listingId = '4471308015'
# token = refreshToken()
# data = getListingDetails(listingId, token)
# # print(json.dumps(data, indent=4))

# StartDate = int(data['StartDate'].strip("/Date()/"))
# AsAt = int(data['AsAt'].strip("/Date()/"))

# timeOnMarket = (AsAt - StartDate)/1000/60/60/24
# print(f'Time on Market is {timeOnMarket} days')