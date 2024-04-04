from getListingDetails import getListingDetails
from refreshToken import refreshToken

def getTimeOnMarket(listingId):

    token = refreshToken()
    data = getListingDetails(listingId, token)

    StartDate = int(data['StartDate'].strip("/Date()/"))
    AsAt = int(data['AsAt'].strip("/Date()/"))

    timeOnMarket = (AsAt - StartDate)/1000/60/60/24

    return timeOnMarket


# Usage
    
listingId = '4423407588'

timeOnMarket = getTimeOnMarket(listingId)

print(f'Time on Market is {timeOnMarket} days')