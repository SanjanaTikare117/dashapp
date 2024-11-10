from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import traceback

# Import preloaded data from data_handler.py (ensure this imports processed DataFrames for both power and voltage)
try:
    from data_access.data_management import csa_power_df, sm_power_df, dese_power_df, csa_voltage_df, sm_voltage_df, dese_voltage_df
except ImportError as e:
    print(f"Error importing data: {e}")
    csa_power_df = sm_power_df = dese_power_df = csa_voltage_df = sm_voltage_df = dese_voltage_df = None

# Initialize FastAPI app
app = FastAPI()

# Allow cross-origin requests
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Function to extract labels (column names) from a dataframe
def get_labels(df: pd.DataFrame) -> List[str]:
    """Extract column labels from a DataFrame."""
    if df is not None and not df.empty:
        return df.columns.tolist()
    return []

# Endpoint to get data and labels for CSA power dataset
@app.get("/csa_power")
async def get_csa_power_data():
    """Fetch and return processed CSA power data and its column labels."""
    if csa_power_df is None:
        return {"detail": "CSA Power data source not found"}

    try:
        df_csa_power = pd.DataFrame({
            "TIME_UTC_Seconds": csa_power_df['TIME [UTC Seconds]'],
            "R_kW": csa_power_df['R[kW]   '],
            "Y_kW": csa_power_df['Y[kW]   '],
            "B_kW": csa_power_df['B[kW]   '],
            "CSA_A_Year": csa_power_df['CSA_A_Year'],
            "CSA_A_Month": csa_power_df['CSA_A_Month'],
            "CSA_A_day": csa_power_df['CSA_A_day'],
            "CSA_A_Hour": csa_power_df['CSA_A_Hour'],
            "CSA_A_datetime": csa_power_df['CSA_A_datetime']
        })
        json_output = df_csa_power.to_dict(orient="records")
        labels = get_labels(df_csa_power)
        return {"labels": labels, "data": json_output}
    except Exception as e:
        print(f"Error processing CSA power data: {e}")
        return {"detail": "Error processing CSA power data"}
    
# Endpoint to get data and labels for dese power dataset
@app.get("/dese_power")
async def get_dese_power_data():
    """Fetch and return processed DESE power data and its column labels."""
    if dese_power_df is None:
        
        return {"detail": "DESE Power data source not found"}

    try:
        print("hey")
        df_dese_power = pd.DataFrame({
            "TIME_UTC_Seconds": dese_power_df['TIME [UTC Seconds]'],
            "R_kW": dese_power_df['R[kW]   '],
            "Y_kW": dese_power_df['Y[kW]   '],
            "B_kW": dese_power_df['B[kW]   '],
            "DESE_A_Year": dese_power_df['DESE_A_Year'],
            "DESE_A_Month": dese_power_df['DESE_A_Month'],
            "DESE_A_day": dese_power_df['DESE_A_day'],
            "DESE_A_Hour": dese_power_df['DESE_A_Hour'],
            "DESE_A_datetime": dese_power_df['DESE_A_datetime']
        })
        json_output = df_dese_power.to_dict(orient="records")
        labels = get_labels(df_dese_power)
        # return {"labels": labels, "data": json_output}
        return {df_dese_power.shape}
    except Exception as e:
        print(f"Error processing DESE power data: {e}")
        return {"detail": "Error processing DESE power data"}


# # Endpoint to get data and labels for SM power dataset
@app.get("/sm_power")
async def get_sm_power_data():
    #return {sm_power_df.shape}
    print("hello")
    """Fetch and return processed SM power data and its column labels."""
    if sm_power_df is None:
        print("hey")
        return {"detail": "SM Power data source not found"}

    try:
        print("dsa")
        df_sm_power = pd.DataFrame({
            "TIME_UTC_Seconds": sm_power_df['TIME [UTC Seconds]'],
            "R_kW": sm_power_df['R[kW]   '],
            "Y_kW": sm_power_df['Y[kW]   '],
            "B_kW": sm_power_df['B[kW]   '],
            "SM_A_Year": sm_power_df['SM_A_Year'],
            "SM_A_Month": sm_power_df['SM_A_Month'],
            "SM_A_day": sm_power_df['SM_A_day'],
            "SM_A_Hour": sm_power_df['SM_A_Hour'],
            "SM_A_datetime": sm_power_df['SM_A_datetime'],
            "SM_A_Minute": sm_power_df['SM_A_Minute']
        })
        json_output = df_sm_power.to_dict(orient="records")
        labels = get_labels(df_sm_power)
        #return {df_sm_power.shape}
        #return {sm_power_df}
        return {"labels": labels,"data":json_output}
    except Exception as e:
        print(f"Error processing SM power data: {e}")
        return {"detail": "Error processing SM power data"}


# Endpoint to get data and labels for CSA voltage dataset
@app.get("/sm_voltage")
async def get_sm_voltage_data():
    # return{sm_voltage_df.shape}
    if sm_voltage_df is None:
        return {"detail": "SM Voltage data source not found"}

    try:
        print("sanj")
        df_sm_voltage = pd.DataFrame({
            "TIME_UTC_Seconds": sm_voltage_df['TIME [UTC Seconds]'],
            "R_Volt": sm_voltage_df[ 'R[Volt]   '],
            "Y_Volt": sm_voltage_df[ 'Y[Volt]   '],
            "B_Volt": sm_voltage_df[ 'B[Volt]   '],
            "SM_A_Voltage_Year": sm_voltage_df[ 'SM_A_Voltage_Year'],
            "SM_A_Voltage_Month": sm_voltage_df[ 'SM_A_Voltage_Month'],
            "SM_A_Voltage_day": sm_voltage_df['SM_A_Voltage_day'],
            "SM_A_Voltage_Hour": sm_voltage_df[ 'SM_A_Voltage_Hour'],
            "SM_A_Voltage_datetime": sm_voltage_df['SM_A_Voltage_datetime'],
            "SM_A_Voltage_Minute": sm_voltage_df[ 'SM_A_Voltage_Minute']
        })
        json_output = df_sm_voltage.to_dict(orient="records")
        labels = get_labels(df_sm_voltage)
        # return {df_sm_voltage.shape}
        # return{sm_voltage_df}
        print(labels)
        return {"labels": labels, "data": json_output}
        
    except Exception as e:
        print(f"Error processing SM voltage data: {e}")
        return {"detail": "Error processing SM voltage data"}


# # Endpoint to get data and labels for CSA voltage dataset
@app.get("/dese_voltage")
async def get_dese_voltage_data():
    if dese_voltage_df is None:
        return {"detail": "Dese Voltage data source not found"}

    try:
        print("sanj")
        df_dese_voltage = pd.DataFrame({
            "TIME_UTC_Seconds": dese_voltage_df['TIME [UTC Seconds]'],
            "R_Volt": dese_voltage_df[ 'R[Volt]   '],
            "Y_Volt": dese_voltage_df[ 'Y[Volt]   '],
            "B_Volt": dese_voltage_df[ 'B[Volt]   '],
            "DESE_A_Year": dese_voltage_df[ 'DESE_A_Voltage_Year'],
            "DESE_A_Month": dese_voltage_df[ 'DESE_A_Voltage_Month'],
            "DESE_A_day": dese_voltage_df[ 'DESE_A_Voltage_day'],
            "DESE_A_Hour": dese_voltage_df[ 'DESE_A_Voltage_Hour'],
            "DESE_A_datetime": dese_voltage_df[ 'DESE_A_Voltage_datetime'],
            "DESE_A_Voltage_Minute": dese_voltage_df[ 'DESE_A_Voltage_Minute']
        })
        json_output = df_dese_voltage.to_dict(orient="records")
        labels = get_labels(df_dese_voltage)
        # return {df_csa_voltage.shape}
        return {"labels": labels, "data": json_output}
        
    except Exception as e:
        print(f"Error processing DESE voltage data: {e}")
        return {"detail": "Error processing CSA voltage data"}


    



