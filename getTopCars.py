import pandas as pd
from piecewise_predict import generate_predict_line
from getCarListings import getCarsJson, manipulate_json


def getTopCars(make, model):

    # Needed for getCarsJson
    search_string = ''

    # Call Trademe API and get data
    cars_json = getCarsJson(make, model, search_string)

    # Manipulate data
    clean_cars_json = manipulate_json(cars_json)

    # Save to df
    df = pd.DataFrame(clean_cars_json)

    # Drop zero value rows
    df = df.dropna(subset=['Value'])

    # Add prediction, norm_resiudals to df
    df = generate_predict_line(df)

    # Calculate normalised residuals
    df['Norm_Residuals'] = (df['Predicted'] - df['Value']) / df['Predicted']

    # get top X results based on normalised residual 
    residuals = df.sort_values(by='Norm_Residuals', ascending=False).head(5)

    return residuals


# Example usage
make = 'BMW'
model = 'X3'

residuals = getTopCars(make, model)

for index, row in residuals.iterrows():
    print(f'{row['Odometer']}: {row['Predicted']}, {row['Value']}, {row['Norm_Residuals']}')
