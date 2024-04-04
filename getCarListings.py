import re
import math
from constructURL import construct_url
from getUsedCars import getUsedCars
from refreshToken import refreshToken
from convert_timestamp import extract_convert_tmstamp

def getCarsJson(make, model, search_string):

    rows_fetched = 0
    total_count = 1
    page = 1

    car_listings = []

    token = refreshToken()
    # token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IkNCM0I0MkY3MDBBMTNFMkVDQkE5NDIzOTYwQUVDRjRERTc4M0Y2QjUiLCJ4NXQiOiJ5enRDOXdDaFBpN0xxVUk1WUs3UFRlZUQ5clUiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2F1dGgudHJhZGVtZS5jby5ueiIsIm5iZiI6MTcwODYyOTEwOCwiaWF0IjoxNzA4NjI5MTA4LCJleHAiOjE3MDg2Mjk3MDgsImF1ZCI6WyJ0cmFkZW1lYXBpIiwia29ydWFwaSJdLCJzY29wZSI6WyJvcGVuaWQiLCJwcm9maWxlIiwiZW1haWwiLCJUcmFkZU1lLk15VHJhZGVNZVJlYWQiLCJUcmFkZU1lLk15VHJhZGVNZVdyaXRlIiwiVHJhZGVNZS5NZXNzYWdlQm9hcmQiLCJUcmFkZU1lLkJpZGRpbmdBbmRCdXlpbmciLCJLb3J1QXBpLlJlYWQiLCJLb3J1QXBpLldyaXRlIiwib2ZmbGluZV9hY2Nlc3MiXSwiYW1yIjpbInB3ZCJdLCJjbGllbnRfaWQiOiJmcmVuZF9jbGllbnQiLCJjbGllbnRfdG1faWQiOiIwQjMwMjZERUQzNTk1ODNFREFDN0RGMzY1NENBMzkyNyIsInN1YiI6IjM1MTk3MzQiLCJhdXRoX3RpbWUiOjE3MDYzNDQ1NDgsImlkcCI6InRyYWRlbWUiLCJyb2xlIjoidXNlciIsInNpZCI6IjUyNDRFRTQxQUQzQ0MzM0NBQkM1MDBEOUI2MkVENkRCIn0.fFiLJy0z0zjB6btVM_Yk4MTlmuX7BXWCokvJ_-zeEBPMh_q7LyECV-MOjAR7788NHcBLe4Cw4R777jC25tkEciR-GbFlxBnKXDgpBNx_aGVY6Ffy6ciYfkkGHxrAeO_ic0f-2UFASNpY5vDYb0yToq73IyeJorzpjeNHKYR8m5Fsa1x5XwHHUbGIAAhZYvKPn6yqHUmX9jHvMN_lwvjYoaekjT9OzDMglwJuXzu9u6YY-CsMxr4Lu0RyVr13uEHqP8sJF9vU-UTEtTODtNP8nQjab2zovnOLKMRrg-DwfAtVd3wJALGpvEY56rMmoLyzduDvD51V3LKcm45SHJ7zIP1OuhUCO-l2qajz5MRR49Mfb6_eJhpc_FcGSXvyOV1k4EJ4AtOcTeGCT870zIIg1y1Fszu5h91QmbiOxY2B_A83HptKJqEzczX1UyoWPXlsCdKMrC5HMr-aX0xSkZPeFnk2PCJW2IrMXayCwt3DP61LX3lJjh8Z8tBjlgHM1w5uArsYXU4iUSyN2pDOelysNspupFfcjjqcEMEfUf0IOaXlRZwOiQ1ub9ADehDyxST7j1MMOv0T3CAT9SQ0EZUr820b561EeO9PWmCFyFb1ATAXffG4AqtMUeh1K3tQQnZlo4OlYPQ7OTFRzq9KUpmRE9h-3MkGPAOxSCqXiq6zMUs'

    while rows_fetched < total_count:

        baseurl = 'https://api.trademe.co.nz/v1/Search/Motors/Used.json'
        
        # Dictionary of query parameters
        query_params = {
            "sort_order": "ExpiryDesc",
            "make": make,
            "model": model,
            "search_string": search_string,
            "page": page,
            "rows": "500"
        }

        # construct url based on query
        full_url = construct_url(baseurl, query_params)

        data = getUsedCars(full_url, token)

        car_listings.extend(data['List'])

        rows_fetched = rows_fetched + data['PageSize']
        total_count = data['TotalCount']

        if rows_fetched < total_count:
            page += 1

    return car_listings

def estimate_main_color(color_name):
    if color_name is None:
        return 'Other'
    color_name = color_name.lower()
    if any(word in color_name for word in ['red', 'burgundy', 'maroon', 'ruby', 'wine', 'scarlet', 'cherry', 'carnelian', 'rosso', 'garnet', 'inferno', 'wildfire']):
        return 'Red'
    elif any(word in color_name for word in ['black', 'noir', 'ebony', 'midnight', 'charcoal', 'ink', 'shadow', 'nero', 'anthracite', 'silhouette', 'dark matter', 'licorice', 'magic black', 'blacl']):
        return 'Black'
    elif any(word in color_name for word in ['blue', 'azure', 'navy', 'denim', 'teal', 'aquamarine', 'turquoise', 'stormy seas', 'blu emozione', 'blu intenso', 'marine', 'oceanmint']):
        return 'Blue'
    elif any(word in color_name for word in ['white', 'cardrona', 'eclipse' , 'alpine', 'ivory', 'pearl', 'cream', 'quartz', 'bianco', 'snow', 'frost', 'moon', 'arctic', 'glacier', 'french vanilla', 'frozen wh', 'svo premium palette meribel whit']):
        return 'White'
    elif any(word in color_name for word in ['silver', 'grey', 'gray', 'polymetal' ,'metallic', 'titanium', 'magnetic', 'graphite', 'knight', 'granite', 'aluminium', 'gunmetal', 'steel', 'platinum', 'silveer', 'tungsten', 'sonic iridium', 'iron metal', 'panthera metal', 'silve', 'sliver', 'gun metalic', 'gunmetalic']):
        return 'Silver'
    elif any(word in color_name for word in ['green', 'olive', 'emerald', 'khaki', 'jungle', 'forest', 'verdant', 'poison ivy', 'regal peacock']):
        return 'Green'
    elif any(word in color_name for word in ['yellow', 'gold', 'amber', 'lemon', 'citrus', 'mustard', 'honey bee', 'grabber lime']):
        return 'Yellow'
    elif any(word in color_name for word in ['orange', 'tangerine', 'coral', 'flame', 'sunset', 'copper', 'alaskan sunset', 'sonic copper', 'hot chilli pepper']):
        return 'Orange'
    elif any(word in color_name for word in ['purple', 'violet', 'lavender', 'lilac', 'mauve', 'purpel', 'purple']):
        return 'Purple'
    elif any(word in color_name for word in ['brown', 'beige', 'tan', 'mocha', 'bronze', 'chocolate', 'sepia', 'toffee', 'marron', 'gobi', 'pua gobi', 'sandstone', 'truffle', 'parchment']):
        return 'Brown'
    elif any(word in color_name for word in ['eclipse', 'ceramic', 'polymetal', 'arctic freeze', 'options available', 'champagne', 'thunder', 'tigre', 'various colours', 'multiple colours available', 'space', 'sonic shade', 'meteor', 'gondwana stone', 'colours to order', 'aluminum', 'grigio lava opaco', 'precious metal', 'basalt mica', 'manganese lustre', 'lots', 'various', 'gun metal', 'absolute', 'sinamon stick', 'moulan rouge', 'various (limited)', 'ooh la la rouge mica', 'ice ecru', 'sterling', 'cobalt', 'special paint', 'brandy', 'crystal garnet', 'magnesium', 'jupiter', '5 colours available', 'peridot', 'nero assoluto', 'nero tempesta', 'radium', 'grigio lava', 'all colours available now!', 'fridge door', 'yello', 'yelow', 'storm bay', 'sonic shade', 'arctic glow', 'ocean view', 'grigio maratea', 'gun metal', 'light taupe', 'zircon sand', 'spring cloud', 'bordeaux', 'champagne', 'g4kmna181464', 'french vanilla', 'panther', 'santorini', 'onyx', 'neptune', 'ceramic tri tone', 'dive in jeju', 'hallmark', 'onyx blac', 'scaret ember', 'rain forrest', 'shooting star', 'dark camouflage', 'arctic dawn', 'liquid mercury', 'luxe', 'ether', 'opal', 'cardroina', 'gondwana stone', 'cool soda', 'plum crazy', 'nitrate', 'beach sand', 'high velocity', 'rocky mountain', 'pewter', 'gun metalic']):
        return 'Other'
    else:
        return 'Other'

def manipulate_json(car_json):

    for item in car_json:

        # Extract and convert price
        match = re.search(r'\$([\d,]+)', item['PriceDisplay'])
        if match:
            item['Price'] = float(match.group(1).replace(',', ''))
        else:
            item['Price'] = None  # or some default value, if PriceDisplay might not have a price

        # Initialize 'Value' with None
        item['Value'] = None

        # Set 'Value' based on other keys
        if item.get('IsClassified', False):
            item['Value'] = item.get('StartPrice', None)  # Using get with default None
        elif item.get('HasBuyNow', False):
            item['Value'] = item.get('BuyNowPrice', None)

        # Update the main colour of the car:
        item['MainColour'] = estimate_main_color(item['ExteriorColour'])

        # Calculate Duration
        StartDate = int(item['StartDate'].strip("/Date()/"))
        AsAt = int(item['AsAt'].strip("/Date()/"))

        item['Duration'] = math.ceil((AsAt - StartDate)/1000/60/60/24)

    return car_json

# # Example usage
# make = 'kia'
# model = 'sportage'
# search_string = ''

# cars_json = getCarsJson(make, model, search_string)
# clean_json = manipulate_json(cars_json)
# import json

# print(len(clean_json))
# for car in clean_json:
#     # if car['ListingId'] == 4532044152 or car['ListingId'] == 4528442378:
#         # nzt_time = extract_convert_tmstamp(car['StartDate'])
#         # print(nzt_time)
#     print(json.dumps(car, indent=4))
#     break
# # print(cars_json[0])
