from getCarListings_R1 import getCarsJson, manipulate_json
from calculateOutliers import z_score
import pandas as pd


def checkIfOutlier(make, model, year, odometer):

    car_json = getCarsJson(make, model, year, odometer)
    clean_cars_json = manipulate_json(car_json)

    df = pd.DataFrame(clean_cars_json)

    df = df.dropna(subset=['Value'])
    

    df['modified_z_score'] = z_score(df['Value'])

    outliers = df[df['modified_z_score'] < -0.5]

    # Example usage
    return outliers

make = 'suzuki'
model = 'kizashi'
odometer = 164373
year = 2011

outliers = checkIfOutlier(make, model, year, odometer)

print(outliers[['Odometer', 'Value','modified_z_score']])
