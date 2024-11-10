import pandas as pd
import glob
import os

class DataProcessorBase:
    def __init__(self, dataset_name, directory, time_col, power_cols):
        self.dataset_name = dataset_name
        self.directory = directory
        self.time_col = time_col
        self.power_cols = power_cols
        self.data = None

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
        if self.data is None or self.data.empty:
            print(f"No data to process for {self.dataset_name}.")
            return None
        
        # Drop unnecessary columns (e.g., 'Unnamed: 4')
        self.data = self.data.drop(columns=['Unnamed: 4'], errors='ignore')
        
        # Ensure numeric columns are correctly formatted
        self.data[self.power_cols] = self.data[self.power_cols].apply(pd.to_numeric, errors='coerce')
        
        # Convert time column to datetime and create additional time-related columns
        self.data[f'{self.dataset_name}_datetime'] = pd.to_datetime(self.data[self.time_col], unit='ms', errors='coerce')
        self.data[f'{self.dataset_name}_Year'] = self.data[f'{self.dataset_name}_datetime'].dt.year
        self.data[f'{self.dataset_name}_Month'] = self.data[f'{self.dataset_name}_datetime'].dt.month
        self.data[f'{self.dataset_name}_day'] = self.data[f'{self.dataset_name}_datetime'].dt.day
        self.data[f'{self.dataset_name}_Hour'] = self.data[f'{self.dataset_name}_datetime'].dt.hour
        self.data[f'{self.dataset_name}_Minute'] = self.data[f'{self.dataset_name}_datetime'].dt.minute
        
        print(f"Data processed for {self.dataset_name}.")
        return self.data

# Specialized class for SM Power data
class PowerDataProcessor(DataProcessorBase):
    def __init__(self, dataset_name, directory):
        power_cols = ["R[kW]   ", "Y[kW]   ", "B[kW]   "]
        super().__init__(dataset_name, directory, "TIME [UTC Seconds]", power_cols)

# Initialize processor for SM power data
sm_power = PowerDataProcessor(dataset_name='SM_A', directory='./data/SoilMech-dataset')

# Load and process SM power data
sm_power.load_data()

# Check if data was loaded before processing
sm_power_df = sm_power.process_data()

# Print to verify if the data has been processed correctly
if sm_power_df is not None:
    print(sm_power_df.head())  # Display head of the processed data
else:
    print("SM Power data not available.")
