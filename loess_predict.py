import numpy as np
import pandas as pd
import statsmodels.api as sm

def generate_loess_predictions(df,frac):
    
    # Sort the DataFrame by 'Odometer' for proper line plotting
    df.sort_values('Odometer', inplace=True)

    # Ensure 'Odometer' is a float64 for the merge
    df['Odometer'] = df['Odometer'].astype('float64')

    # Extract the 'Odometer' and 'Value' columns for LOESS
    x = df['Odometer'].values
    y = df['Value'].values

    # Fit the LOESS model
    lowess = sm.nonparametric.lowess
    loess_results = lowess(y, x, frac=frac)

    # The returned values from lowess are a 2-column array with the first column
    # being the sorted 'x' and the second column the corresponding predicted 'y'
    predicted_x = loess_results[:, 0]
    predicted_y = loess_results[:, 1]

    # Add the LOESS predictions to the DataFrame
    df_loess = pd.DataFrame({
        'Odometer': predicted_x,
        'Predicted': predicted_y
    })

    # Merge the LOESS predictions with the original DataFrame
    df_merged = pd.merge_asof(df.sort_values('Odometer'), df_loess.sort_values('Odometer'), on='Odometer', direction='nearest')

    return df_merged

# # Load JSON into a pandas DataFrame
# df = pd.read_json('Audi_Q5_2024-01-30.json')

# df = df.dropna(subset=['Value'])

# df = generate_loess_predictions(df, 0.3)

# # Calculate normalised residuals
# df['Norm_Residuals'] = (df['Predicted'] - df['Value']) / df['Predicted']

# # get top X results based on normalised residual 
# residuals = df.sort_values(by='Norm_Residuals', ascending=False).head(5)

# print(residuals)
