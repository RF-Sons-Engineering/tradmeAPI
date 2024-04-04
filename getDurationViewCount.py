from convert_timestamp import extract_convert_tmstamp

def getDurationViewCount(listingJson, unit):
    
    if unit == 'hrs':
        divider = 3600
    elif unit == 'days':
        divider = 3600*24

    
    StartDate = extract_convert_tmstamp(listingJson['StartDate'])
    AsAt = extract_convert_tmstamp(listingJson['AsAt'])
    Duration = (AsAt - StartDate).total_seconds()/divider
    ViewCount = listingJson['ViewCount']

    return Duration, ViewCount


# # Example usage
# from getListingDetails import getListingDetails
# from refreshToken import refreshToken

# listingId = '4536393353'
# token = refreshToken()
# listingJson = getListingDetails(listingId, token)
# Duration, ViewCount = getDurationViewCount(listingJson, 'days')

# print(f"Time on the market: {round(Duration,2)} days, Views per day: {round(ViewCount, 2)}")