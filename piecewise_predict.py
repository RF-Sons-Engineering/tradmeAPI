import numpy as np
import statsmodels.api as sm
from scipy.optimize import minimize

# Function to calculate the total sum of squares error for a given breakpoint
def ssr(breakpoint, df):

    # Extract the scalar value from the breakpoint array
    breakpoint = breakpoint[0]

    # Ensure breakpoint is within the range of odometer readings to avoid empty segments
    if breakpoint < df['Odometer'].min() or breakpoint > df['Odometer'].max():
        return np.inf

    # Data below the breakpoint
    lower_data = df[df['Odometer'] <= breakpoint]
    X_lower = sm.add_constant(lower_data['Odometer'])
    model_lower = sm.OLS(lower_data['Value'], X_lower).fit()

    # Data above the breakpoint
    upper_data = df[df['Odometer'] > breakpoint]
    X_upper = sm.add_constant(upper_data['Odometer'])
    model_upper = sm.OLS(upper_data['Value'], X_upper).fit()

    # Sum of squared residuals
    ssr_total = model_lower.ssr + model_upper.ssr
    return ssr_total


def generate_predict_line(df):

    # Initial guess for the breakpoint
    initial_breakpoint = df['Odometer'].median()

    # Optimization to minimize the SSR with respect to the breakpoint
    result = minimize(fun=ssr, x0=initial_breakpoint, args=(df,), method='Nelder-Mead')

    # The optimal breakpoint
    optimal_breakpoint = result.x[0]

    # Now use the optimal_breakpoint to fit your final piecewise regression model
    # and evaluate its performance

    # Create a new column for the piecewise function
    df['Piecewise'] = np.where(df['Odometer'] > optimal_breakpoint, df['Odometer'] - optimal_breakpoint, 0)

    # Fit the piecewise regression model
    X = df[['Odometer', 'Piecewise']]
    X = sm.add_constant(X)  # Adds a constant term to the predictor
    y = df['Value']

    model = sm.OLS(y, X).fit()
    # print(model.summary())

    # Get the model's predictions
    df['Predicted'] = model.predict(X)

    # Sort the DataFrame by 'odometer' for proper line plotting
    df.sort_values('Odometer', inplace=True)

    return df

# # Example usage
# import pandas as pd

# # Load JSON into a pandas DataFrame
# df = pd.read_json('Audi_Q5_2024-01-30.json')

# df = df.dropna(subset=['Value'])

# df = generate_predict_line(df)

