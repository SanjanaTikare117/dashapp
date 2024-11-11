from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from data_access.data_management import csa_power_df, sm_power_df, dese_power_df, csa_voltage_df, sm_voltage_df, dese_voltage_df
from data_access.data_processing import process_csa_power_data, process_dese_power_data, process_sm_power_data, process_sm_voltage_data, process_dese_voltage_data, process_csa_voltage_data

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

@app.get("/csa_power")
async def get_csa_power_data():
    """Fetch and return processed CSA power data and its column labels."""
    if csa_power_df is None:
        return {"detail": "CSA Power data source not found"}
    return process_csa_power_data(csa_power_df)

@app.get("/dese_power")
async def get_dese_power_data():
    """Fetch and return processed DESE power data and its column labels."""
    if dese_power_df is None:
        return {"detail": "DESE Power data source not found"}
    return process_dese_power_data(dese_power_df)

@app.get("/sm_power")
async def get_sm_power_data():
    """Fetch and return processed SM power data and its column labels."""
    if sm_power_df is None:
        return {"detail": "SM Power data source not found"}
    return process_sm_power_data(sm_power_df)

@app.get("/sm_voltage")
async def get_sm_voltage_data():
    """Fetch and return processed SM voltage data and its column labels."""
    if sm_voltage_df is None:
        return {"detail": "SM Voltage data source not found"}
    return process_sm_voltage_data(sm_voltage_df)

@app.get("/csa_voltage")
async def get_csa_voltage_data():
    """Fetch and return processed CSA voltage data and its column labels."""
    if csa_voltage_df is None:  # Corrected the check to csa_voltage_df
        return {"detail": "CSA Voltage data source not found"}
    return process_csa_voltage_data(csa_voltage_df)  # Passing the correct DataFrame

@app.get("/dese_voltage")
async def get_dese_voltage_data():
    """Fetch and return processed DESE voltage data and its column labels."""
    if dese_voltage_df is None:
        return {"detail": "DESE Voltage data source not found"}
    return process_dese_voltage_data(dese_voltage_df)
