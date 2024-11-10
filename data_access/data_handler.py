import pandas as pd
import numpy as np
from pathlib import Path
import glob
import os

class DataProcessorBase:
    def __init__(self, dataset_name, directory, time_col, power_cols):
        self.dataset_name = dataset_name
        self.directory = directory
        self.time_col = time_col
        self.power_cols = power_cols
        self.data = None
        self.feather_path = f'./data/{dataset_name}_data.feather'  # Path for Feather file

    def load_data(self, skip_rows=6, use_columns=[0, 1, 2, 3, 4]):
        csv_files = glob.glob(os.path.join(self.directory, '*.csv'))
        print(f"Found CSV files in {self.directory}: {csv_files}")

        dfs = []
        for csv_file in csv_files:
            try:
                data = pd.read_csv(csv_file, skiprows=skip_rows, usecols=use_columns)
                dfs.append(data)
            except pd.errors.ParserError as e:
                print(f"Error reading {csv_file}: {e}")

        if dfs:
            self.data = pd.concat(dfs, axis=0, ignore_index=True)
            print(f"Data loaded for {self.dataset_name}.")
        else:
            print(f"No data loaded for {self.dataset_name}. Check your file paths or CSV files.")

    def process_data(self):
        if self.data is None:
            print(f"No data to process for {self.dataset_name}.")
            return
        
        # Convert time column to datetime and create additional time-related columns
        self.data[f'{self.dataset_name}_datetime'] = pd.to_datetime(self.data[self.time_col], unit='ms')
        self.data[f'{self.dataset_name}_Year'] = self.data[f'{self.dataset_name}_datetime'].dt.year
        self.data[f'{self.dataset_name}_Month'] = self.data[f'{self.dataset_name}_datetime'].dt.month
        self.data[f'{self.dataset_name}_day'] = self.data[f'{self.dataset_name}_datetime'].dt.day
        self.data[f'{self.dataset_name}_Hour'] = self.data[f'{self.dataset_name}_datetime'].dt.hour
        self.data[f'{self.dataset_name}_Minute'] = self.data[f'{self.dataset_name}_datetime'].dt.minute
        print(f"Data processed for {self.dataset_name}.")

    def save_data_feather(self):
        os.makedirs('./data', exist_ok=True)  # Ensure the directory exists
        if self.data is not None:
            self.data.to_feather(self.feather_path)
            print(f"{self.dataset_name} data saved to {self.feather_path}.")
        else:
            print(f"No data to save for {self.dataset_name}.")

    def load_feather_data(self):
        if os.path.exists(self.feather_path):
            self.data = pd.read_feather(self.feather_path)
            print(f"{self.dataset_name} data loaded from {self.feather_path}.")
        else:
            print(f"No Feather file found for {self.dataset_name} at {self.feather_path}.")


# Specialized classes for power and voltage datasets
class PowerDataProcessor(DataProcessorBase):
    def __init__(self, dataset_name, directory):
        power_cols = ["R[kW]   ", "Y[kW]   ", "B[kW]   "]
        super().__init__(dataset_name, directory, "TIME [UTC Seconds]", power_cols)

class VoltageDataProcessor(DataProcessorBase):
    def __init__(self, dataset_name, directory):
        power_cols = ["R[Volt]   ", "Y[Volt]   ", "B[Volt]   "]
        super().__init__(dataset_name, directory, "TIME [UTC Seconds]", power_cols)

# Initialize processors for power and voltage data
csa_power = PowerDataProcessor(dataset_name='CSA_A', directory='./data/Csa.csv')
sm_power = PowerDataProcessor(dataset_name='SM_A', directory='./data/SoilMech-dataset')
dese_power = PowerDataProcessor(dataset_name='DESE_A', directory='./data/Dese.csv')

csa_voltage = VoltageDataProcessor(dataset_name='CSA_V', directory='./data/csavoltage.dataset')
sm_voltage = VoltageDataProcessor(dataset_name='SM_V', directory='./data/SMvoltagedataset')
dese_voltage = VoltageDataProcessor(dataset_name='DESE_V', directory='./data/desevoltage.csv')

# Process and save data
for processor in [csa_power, sm_power, dese_power, csa_voltage, sm_voltage, dese_voltage]:
    processor.load_data()        # Load the CSV data
    processor.process_data()     # Process the loaded data (e.g., time conversion)
    processor.save_data_feather()  # Save to Feather format


import pandas as pd
csa_power_data = pd.read_feather('./data/')
csa_power_data.head()