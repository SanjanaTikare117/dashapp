import pandas as pd
import os
import sys
import asyncio

# Adding the parent directory to the system path to import functions from app_test
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importing data fetching functions
from app_test import (get_csa_power_data, get_sm_power_data, get_dese_power_data, get_csa_voltage_data, get_sm_voltage_data, get_dese_voltage_data)

class DataFetcher:
    def __init__(self):
        # Dictionary mapping data sources to their respective async data fetch functions
        self.data_sources = {'CSA_Power': get_csa_power_data, 'SM_Power': get_sm_power_data, 'DESE_Power': get_dese_power_data, 'CSA_Voltage': get_csa_voltage_data,  'SM_Voltage': get_sm_voltage_data, 'DESE_Voltage': get_dese_voltage_data }
    
    async def fetch_data(self, source_name):
        """Fetch data asynchronously from the given source."""
        if source_name in self.data_sources:
            fetch_func = self.data_sources[source_name]
            data = await fetch_func()
            return data
        else:
            raise ValueError(f"Data source '{source_name}' not found.")
    
    def preprocess_dataframe(self, data, datetime_column):
        """Preprocess data and return the DataFrame with datetime index set."""
        # Create DataFrame directly from fetched data
        if isinstance(data, dict) and 'data' in data:
            df = pd.DataFrame(data['data'])
        elif isinstance(data, (tuple, set)):
            df = pd.DataFrame(list(data))
        else:
            raise ValueError("Unsupported data format received.")

        # Check if the datetime column exists in the data and set it as the index
        if datetime_column in df.columns:
            df['datetime'] = pd.to_datetime(df[datetime_column])
            df.set_index('datetime', inplace=True)
        else:
            raise ValueError(f"The specified datetime column '{datetime_column}' was not found in the data.")

        return df

    async def fetch_and_process(self, source_name, datetime_column):
        """Fetch and preprocess data for a given source."""
        print(f"Fetching data for {source_name}...")
        try:
            raw_data = await self.fetch_data(source_name)
            processed_df = self.preprocess_dataframe(raw_data, datetime_column)
            print(f"Data for {source_name} fetched and processed successfully.\n")
            return processed_df
        except Exception as e:
            print(f"Error fetching or processing data for {source_name}: {e}")
            return None

async def main():
    fetcher = DataFetcher()
    
    # Define the data sources and their respective datetime columns
    data_sources = [ ("CSA_Power", "CSA_A_datetime"), 
        ("SM_Power", "SM_A_datetime"),
        ("DESE_Power", "DESE_A_datetime"),
        ("CSA_Voltage", "CSA_A_datetime"),
        ("SM_Voltage", "SM_A_datetime"),
        ("DESE_Voltage", "DESE_A_datetime")
    ]
    
    results = {}
    for source_name, datetime_column in data_sources:
        processed_df = await fetcher.fetch_and_process(source_name, datetime_column)
        if processed_df is not None:
            results[source_name] = processed_df
            # Display the first few rows of each DataFrame for verification
            print(f"{source_name} Data:\n", processed_df.head())

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())
