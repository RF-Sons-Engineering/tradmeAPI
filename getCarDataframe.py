import pandas as pd
from constructURL import construct_url
from getUsedCars import getUsedCars
from refreshToken import refreshToken

def getListings(make, model):

    rows_fetched = 0
    total_count = 1
    page = 1

    car_listings = []

    while rows_fetched < total_count:

        # Dictionary of query parameters
        query_params = {
            "sort_order": "ExpiryDesc",
            "make": make,
            "model": model,
            "page": page,
            "rows": "500"
        }

        # construct url based on query
        full_url = construct_url(query_params)

        token = refreshToken()

        data = getUsedCars(full_url, token)

        car_listings.extend(data['List'])

        rows_fetched = rows_fetched + data['PageSize']
        total_count = data['TotalCount']

        if rows_fetched < total_count:
            page += 1

    
    df = pd.DataFrame(car_listings)

    return df


# # Example usage
# make = 'audi'
# model = 'a3'

# df = getListings(make, model)
# print(df.columns)

# for index, row in df.iterrows():
#     print(row)
#     break