# data_analysis/plotter.py
import plotly.express as px
import plotly.graph_objects as go

def create_bar_plot(data, parameter):
    """Create a bar plot."""
    return px.bar(data, x=data.index, y=parameter)

def create_line_plot(data, parameter):
    """Create a line plot."""
    return px.line(data, x=data.index, y=parameter)

def create_heatmap(data, parameter):
    """Create a heatmap for hourly data."""
    # Resample the data to hourly frequency
    df_hourly = data.resample('H').mean()
    # Assuming 24 hours of data per day
    heatmap_data = df_hourly[parameter].values.reshape(-1, 24)
    
    # Create and return heatmap figure
    return go.Figure(data=go.Heatmap(z=heatmap_data))
