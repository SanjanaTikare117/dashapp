import pandas as pd
import numpy as np
import os
import sys
import asyncio

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app_test import get_csa_power_data

# def generate_dummy_data():
#     date_range = pd.date_range(start='2023-01-01', end='2023-12-31', freq='H')
#     df = pd.DataFrame({
#         'datetime': date_range,
#         'Total Active Power': np.random.uniform(100, 500, len(date_range)),
#         'Total Voltage': np.random.uniform(220, 240, len(date_range))
#     })
#     return df

#df = generate_dummy_data()
#df = await get_csa_power_data()

def preprocess_dataframe(data, value_column):
    df = pd.DataFrame(data['data'])
    df['datetime'] = pd.to_datetime(df['CSA_A_datetime'])
    df.set_index('datetime', inplace=True)
    numeric_cols = df.select_dtypes(include=['number']).columns
    df_hourly = df[numeric_cols].resample('h').mean()
    daily_data = df[numeric_cols].resample('D').agg({
        value_column: ['min', 'max', 'mean']
    })
    daily_data.columns = ['min', 'max', 'mean']
    daily_data = daily_data.reset_index()
    
    #print(df['labels'])
    #print(df['data'])
    #print(data)
    return df, daily_data

#combined_df, combined_daily_data = preprocess_dataframe(df, 'Total Active Power')






# Assuming get_csa_power_data is an async function that fetches data
async def fetch_and_process_data():
    df = await get_csa_power_data()  # Await the asynchronous function
    print('Inside fetch function')
    combined_df, combined_daily_data = preprocess_dataframe(df, 'Total Active Power')
    return combined_df, combined_daily_data

# Run the asynchronous function
async def main():
    print("Inside main function")
    combined_df, combined_daily_data = await fetch_and_process_data()
    print(combined_df.head())  # For testing the output

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())
