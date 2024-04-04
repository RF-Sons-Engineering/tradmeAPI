import requests
from constructURL import construct_url
from refreshToken import refreshToken
from convert_timestamp import extract_convert_tmstamp

def getExpiredListings(query_params, token):

    baseurl = 'https://api.trademe.co.nz/v1/Search/General.json'

    # construct url based on query
    full_url = construct_url(baseurl, query_params)

    headers = {
    'Authorization': f'Bearer {token}'
    }

    response = requests.request("GET", full_url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return response.text


import json

# Example usage
# Dictionary of query parameters
query_params = {
    # "sort_order": "MotorsLatestListings",
    "category": "0001-0268-0334-",
    "search_string": "",
    "expired": 0,
    "page": 1,
    "rows": "50",
    "return_metadata": True
}

token = refreshToken()

data = getExpiredListings(query_params, token)

# print(data)
# for item in data['List']:
    # print(f'{item['ListingId']}: {extract_convert_tmstamp(item['StartDate'])} / {extract_convert_tmstamp(item['EndDate'])}')

print(json.dumps(data['List'][0], indent=4))