import glob
import os
import pandas as pd

# Base class for data processing
class DataProcessorBase:
    def __init__(self, dataset_name, directory, time_col, power_cols, voltage_cols=None):
        self.dataset_name = dataset_name
        self.directory = directory
        self.time_col = time_col
        self.power_cols = power_cols
        self.voltage_cols = voltage_cols
        self.data = None

    def load_data(self, skip_rows=6, use_columns=[0, 1, 2, 3, 4]):
        # Find all CSV files in the specified directory
        csv_files = glob.glob(os.path.join(self.directory, '*.csv'))
        print(f"Found CSV files in {self.directory}: {csv_files}")

        dfs = []
        for csv_file in csv_files:
            try:
                # Try reading the CSV file with given parameters
                data = pd.read_csv(csv_file, skiprows=skip_rows, usecols=use_columns)
                if not data.empty:
                    dfs.append(data)
                else:
                    print(f"Warning: {csv_file} is empty.")
            except pd.errors.ParserError as e:
                print(f"Error reading {csv_file}: {e}")

        if dfs:
            # Concatenate all loaded CSV data
            self.data = pd.concat(dfs, axis=0, ignore_index=True)
            print(f"Data loaded for {self.dataset_name}.")
        else:
            print(f"No data loaded for {self.dataset_name}. Check your file paths or CSV files.")

    def process_data(self):
        # Check if data was loaded before processing
        if self.data is None or self.data.empty:
            print(f"No data to process for {self.dataset_name}.")
            return None
        
        # Convert time column to datetime and create additional time-related columns
        self.data[f'{self.dataset_name}_datetime'] = pd.to_datetime(self.data[self.time_col], unit='ms')
        self.data[f'{self.dataset_name}_Year'] = self.data[f'{self.dataset_name}_datetime'].dt.year
        self.data[f'{self.dataset_name}_Month'] = self.data[f'{self.dataset_name}_datetime'].dt.month
        self.data[f'{self.dataset_name}_day'] = self.data[f'{self.dataset_name}_datetime'].dt.day
        self.data[f'{self.dataset_name}_Hour'] = self.data[f'{self.dataset_name}_datetime'].dt.hour
        self.data[f'{self.dataset_name}_Minute'] = self.data[f'{self.dataset_name}_datetime'].dt.minute
        print(f"Data processed for {self.dataset_name}.")
        return self.data

    def save_to_feather(self, filename):
        # Save processed data to Feather format
        if self.data is not None:
            self.data.reset_index(drop=True, inplace=True)
            self.data.to_feather(filename)
            print(f"Data saved to Feather format at {filename}.")
        else:
            print("No data available to save.")

    def load_from_feather(self, filename):
        # Load data from Feather file
        if os.path.exists(filename):
            df = pd.read_feather(filename)
            print(f"Data loaded from Feather file at {filename}.")
            return df
        else:
            print(f"Feather file not found at {filename}.")

# Specialized class for processing power datasets
class PowerDataProcessor(DataProcessorBase):
    def __init__(self, dataset_name, directory):
        power_cols = ["R[kW]   ", "Y[kW]   ", "B[kW]   "]  # Power columns
        super().__init__(dataset_name, directory, "TIME [UTC Seconds]", power_cols)

# Specialized class for processing voltage datasets
class VoltageDataProcessor(DataProcessorBase):
    def __init__(self, dataset_name, directory):
        voltage_cols = ["R[Volt]   ", "Y[Volt]   ", "B[Volt]   "]  # Voltage columns
        super().__init__(dataset_name, directory, "TIME [UTC Seconds]", voltage_cols, voltage_cols=voltage_cols)

# Initialize processors for CSA, SM, DESE power and voltage datasets
csa_power = PowerDataProcessor(dataset_name='CSA_A', directory='./data/Csa.csv')
sm_power = PowerDataProcessor(dataset_name='SM_A', directory='./data/SoilMech-dataset')
dese_power = PowerDataProcessor(dataset_name='DESE_A', directory='./data/Dese.csv/DESE-dataset')

csa_voltage = VoltageDataProcessor(dataset_name='CSA_A_Voltage', directory='./data/csavoltage.dataset')
sm_voltage = VoltageDataProcessor(dataset_name='SM_A_Voltage', directory='./data/SMvoltagedataset')
dese_voltage = VoltageDataProcessor(dataset_name='DESE_A_Voltage', directory='./data/desevoltage.csv')

# Load and process power and voltage data for each dataset
csa_power.load_data()
sm_power.load_data()
dese_power.load_data()

csa_voltage.load_data()
sm_voltage.load_data()
dese_voltage.load_data()

# Process the data only if it was successfully loaded
csa_power_df = csa_power.process_data()
sm_power_df = sm_power.process_data()
dese_power_df = dese_power.process_data()

csa_voltage_df = csa_voltage.process_data()
sm_voltage_df = sm_voltage.process_data()
dese_voltage_df = dese_voltage.process_data()

# Save processed data to Feather format
csa_power.save_to_feather('./data/csa_power.feather')
sm_power.save_to_feather('./data/sm_power.feather')
dese_power.save_to_feather('./data/dese_power.feather')

csa_voltage.save_to_feather('./data/csa_voltage.feather')
sm_voltage.save_to_feather('./data/sm_voltage.feather')
dese_voltage.save_to_feather('./data/dese_voltage.feather')

# Example of accessing and loading processed Feather data
csa_power.load_from_feather('./data/csa_power.feather')
sm_power.load_from_feather('./data/sm_power.feather')
dese_power.load_from_feather('./data/dese_power.feather')

csa_voltage.load_from_feather('./data/csa_voltage.feather')
sm_voltage.load_from_feather('./data/sm_voltage.feather')
dese_voltage.load_from_feather('./data/dese_voltage.feather')


# Example of accessing processed data
if csa_power.data is not None:
    print("CSA Power Data:")
    print(csa_power.data.head())
else:
    print("CSA Power data not available.")

if sm_power.data is not None:
    print("SM Power Data:")
    print(sm_power.data.head())
else:
    print("SM Power data not available.")

if dese_power.data is not None:
    print("DESE Power Data:")
    print(dese_power.data.head())
else:
    print("DESE Power data not available.")

if csa_voltage.data is not None:
    print("CSA Voltage Data:")
    print(csa_voltage.data.head())
else:
    print("CSA Voltage data not available.")

if sm_voltage.data is not None:
    print("SM Voltage Data:")
    print(sm_voltage.data.head())
else:
    print("SM Voltage data not available.")

if dese_voltage.data is not None:
    print("DESE Voltage Data:")
    print(dese_voltage.data.head())
else:
    print("DESE Voltage data not available.")
