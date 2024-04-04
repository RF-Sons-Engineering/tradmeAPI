import requests

def getUsedCars(url, token):

    headers = {
    'Authorization': f'Bearer {token}'
    }

    response = requests.request("GET", url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return response.text


# Example usage
# url = 'https://api.trademe.co.nz/v1/Search/Motors/Used.json?sort_order=ExpiryDesc&page=1&rows=50'
# data = getUsedCars(url)

# print(data)
# for item in data['List']:
#     print(item['Title'])
