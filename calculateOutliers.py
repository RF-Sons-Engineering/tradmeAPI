import pandas as pd
import numpy as np
import plotly.express as px

def z_score(values):
    mean_val = np.mean(values)
    std_val = np.std(values)
    if std_val == 0:  # Handling the case when standard deviation is 0 to avoid division by zero
        z_scores = np.zeros_like(values)
    else:
        z_scores = (values - mean_val) / std_val
    
    return z_scores

# Function to calculate Modified Z-Score
def modified_z_score(values):
    median_val = np.median(values)
    mad_val = np.median(np.abs(values - median_val))
    if mad_val == 0:  # Handling the case when MAD is 0 to avoid division by zero
        modified_z_scores = np.zeros_like(values)
    else:
        modified_z_scores = 0.6745 * (values - median_val) / mad_val
    
    return modified_z_scores

def calculateOutliers(df, window_size, step):
    # Initialize the DataFrame to store outliers
    outliers = pd.DataFrame()

    # Define the start and end points for the odometer values
    start_point = df['Odometer'].min()
    end_point = df['Odometer'].max()

    # Loop through the odometer values with the defined step
    for start in range(start_point, end_point, step):

        end = start + window_size

        # Select the data within the current window
        window_data = df[(df['Odometer'] >= start) & (df['Odometer'] < end)].copy()

        # Skip the iteration if window_data is empty or we have less than 10 values
        if (not window_data.empty) and (len(window_data) > 10):

            # Print the data in the current window
            # print(window_data[['Odometer', 'Value', 'Year']])

            # Calculate the Modified Z-Score for the 'Value' column
            window_data['modified_z_score'] = z_score(window_data['Value'])
            

            # # Check if there are values with a modified_z_score greater than 3
            # if any(window_data['Odometer'] == 74250):
            #     print(window_data[['Odometer', 'Value','modified_z_score']])

            #     # Filter out the values with a modified_z_score greater than 3
            #     filtered_values = window_data[window_data['modified_z_score'] <= 3]['Value']
                
            #     # Recalculate the Modified Z-Score without the outliers
            #     window_data.loc[window_data['modified_z_score'] <= 3, 'modified_z_score'] = modified_z_score(filtered_values)

            #     if 39260 in window_data['Odometer'].values:
            #         print(window_data[['Odometer', 'Value','modified_z_score']])

            # Identify the outliers in the window
            window_outliers = window_data[window_data['modified_z_score'] < -2.5]
            # if not window_outliers.empty and 39260 in window_outliers['Odometer'].values:
            #     print(window_data[['Odometer', 'Value','modified_z_score']])
            #     print('---')
            outliers = pd.concat([outliers, window_outliers], ignore_index=True)
            # print(outliers[['Odometer', 'Value', 'Year', 'modified_z_score']])


    # Removing duplicate outliers that might appear in overlapping windows
    outliers.drop_duplicates(subset=['ListingId'], inplace=True)

    # The outliers DataFrame now contains the outliers from each window
    return outliers

# # Example usage
# # Ensure that you have the getCarsJson and manipulate_json functions implemented correctly.
# from getCarListings import getCarsJson, manipulate_json

# make_list = ['mazda', 'mazda', 'hyundai']
# model_list = ['demio', 'cx-5', 'tucson']
# search_string = ''

# for index in range(0,6):
    
#     make = make_list[index]
#     model = model_list[index]
#     print(f'{make}, {model}')
#     cars_json = getCarsJson(make, model, search_string)
#     clean_cars_json = manipulate_json(cars_json)
#     df = pd.DataFrame(clean_cars_json)
#     # Drop NA values from Value column
#     df = df.dropna(subset=['Value'])

#     # Define window size and stepe
#     window_size = 20000  # This can be adjusted based on your specific needs
#     step = 1000  # This can also be adjusted based on your specific needs

#     # Example usage
#     outliers = calculateOutliers(df, window_size, step)
#     outliers.sort_values('modified_z_score', inplace=True)
#     print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
#     print(outliers[['Odometer', 'Value', 'Year', 'modified_z_score']])

# # # Plotting
# # fig1 = px.scatter(df, x='Odometer', y='Value', color='MainColour', custom_data=['ListingId'])
# # # fig1.show()
