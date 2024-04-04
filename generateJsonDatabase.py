from getCarListings import getCarsJson, manipulate_json
from refreshToken import refreshToken
from getListingDetails import getListingDetails
from getDurationViewCount import getDurationViewCount
from datetime import datetime
import json

make = 'Audi'
model = 'Q5'
search_string = ''

cars_json = getCarsJson(make, model, search_string)
clean_json = manipulate_json(cars_json)
token = refreshToken()
i = 0
nCars = len(clean_json)
for car in clean_json:
    i = i + 1
    print(f'{i}/{nCars}')
    listingId = car['ListingId']
    listingJson = getListingDetails(listingId, token)
    Duration, ViewCount = getDurationViewCount(listingJson, 'days')
    car['Duration'] = Duration
    car['ViewCount'] = ViewCount

date_str = datetime.now().strftime('%Y-%m-%d')
filename = f'{make}_{model}_{date_str}.json'

# Write JSON data to file
with open(filename, 'w') as file:
    json.dump(clean_json, file, indent=4)