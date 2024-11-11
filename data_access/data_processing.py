import pandas as pd
from data_access.label_handler import get_labels

def process_csa_power_data(csa_power_df: pd.DataFrame):
    """Process CSA power data and return labels and data."""
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
        labels = get_labels(df_csa_power)  # Extract labels using the helper function
        return {"labels": labels, "data": json_output}
    
    except Exception as e:
        print(f"Error processing CSA power data: {e}")
        return {"detail": "Error processing CSA power data"}


def process_dese_power_data(dese_power_df: pd.DataFrame):
    """Process DESE power data and return labels and data."""
    try:
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
        labels = get_labels(df_dese_power)  # Extract labels using the helper function
        return {"labels": labels, "data": json_output}
    
    except Exception as e:
        print(f"Error processing DESE power data: {e}")
        return {"detail": "Error processing DESE power data"}


def process_sm_power_data(sm_power_df: pd.DataFrame):
    """Process SM power data and return labels and data."""
    try:
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
        labels = get_labels(df_sm_power)  # Extract labels using the helper function
        return {"labels": labels, "data": json_output}
    
    except Exception as e:
        print(f"Error processing SM power data: {e}")
        return {"detail": "Error processing SM power data"}


def process_sm_voltage_data(sm_voltage_df: pd.DataFrame):
    """Process SM voltage data and return labels and data."""
    try:
        df_sm_voltage = pd.DataFrame({
            "TIME_UTC_Seconds": sm_voltage_df['TIME [UTC Seconds]'],
            "R_Volt": sm_voltage_df['R[Volt]   '],
            "Y_Volt": sm_voltage_df['Y[Volt]   '],
            "B_Volt": sm_voltage_df['B[Volt]   '],
            "SM_A_Voltage_Year": sm_voltage_df['SM_A_Voltage_Year'],
            "SM_A_Voltage_Month": sm_voltage_df['SM_A_Voltage_Month'],
            "SM_A_Voltage_day": sm_voltage_df['SM_A_Voltage_day'],
            "SM_A_Voltage_Hour": sm_voltage_df['SM_A_Voltage_Hour'],
            "SM_A_Voltage_datetime": sm_voltage_df['SM_A_Voltage_datetime'],
            "SM_A_Voltage_Minute": sm_voltage_df['SM_A_Voltage_Minute']
        })
        json_output = df_sm_voltage.to_dict(orient="records")
        labels = get_labels(df_sm_voltage)  # Extract labels using the helper function
        return {"labels": labels, "data": json_output}
    
    except Exception as e:
        print(f"Error processing SM voltage data: {e}")
        return {"detail": "Error processing SM voltage data"}
    
    
def process_csa_voltage_data(csa_voltage_df: pd.DataFrame):
    """Process SM voltage data and return labels and data."""
    try:
        df_csa_voltage = pd.DataFrame({
            "TIME_UTC_Seconds": csa_voltage_df['TIME [UTC Seconds]'],
            "R_Volt": csa_voltage_df['R[Volt]   '],
            "Y_Volt": csa_voltage_df['Y[Volt]   '],
            "B_Volt": csa_voltage_df['B[Volt]   '],
            "CSA_A_Voltage_Year": csa_voltage_df['CSA_A_Voltage_Year'],
            "CSA_A_Voltage_Month": csa_voltage_df['CSA_A_Voltage_Month'],
            "CSA_A_Voltage_day": csa_voltage_df['CSA_A_Voltage_day'],
            "CSA_A_Voltage_Hour": csa_voltage_df['CSA_A_Voltage_Hour'],
            "CSA_A_Voltage_datetime": csa_voltage_df['CSA_A_Voltage_datetime'],
            "CSA_A_Voltage_Minute": csa_voltage_df['CSA_A_Voltage_Minute']
        })
        json_output = df_csa_voltage.to_dict(orient="records")
        labels = get_labels(df_csa_voltage)  # Extract labels using the helper function
        return {"labels": labels, "data": json_output}
    
    except Exception as e:
        print(f"Error processing CSA voltage data: {e}")
        return {"detail": "Error processing SM voltage data"}


def process_dese_voltage_data(dese_voltage_df: pd.DataFrame):
    """Process DESE voltage data and return labels and data."""
    try:
        df_dese_voltage = pd.DataFrame({
            "TIME_UTC_Seconds": dese_voltage_df['TIME [UTC Seconds]'],
            "R_Volt": dese_voltage_df['R[Volt]   '],
            "Y_Volt": dese_voltage_df['Y[Volt]   '],
            "B_Volt": dese_voltage_df['B[Volt]   '],
            "DESE_A_Year": dese_voltage_df['DESE_A_Voltage_Year'],
            "DESE_A_Month": dese_voltage_df['DESE_A_Voltage_Month'],
            "DESE_A_day": dese_voltage_df['DESE_A_Voltage_day'],
            "DESE_A_Hour": dese_voltage_df['DESE_A_Voltage_Hour'],
            "DESE_A_datetime": dese_voltage_df['DESE_A_Voltage_datetime'],
            "DESE_A_Voltage_Minute": dese_voltage_df['DESE_A_Voltage_Minute']
        })
        json_output = df_dese_voltage.to_dict(orient="records")
        labels = get_labels(df_dese_voltage)  # Extract labels using the helper function
        return {"labels": labels, "data": json_output}
    
    except Exception as e:
        print(f"Error processing DESE voltage data: {e}")
        return {"detail": "Error processing DESE voltage data"}
