import asyncio
from dash import Input, Output
import plotly.express as px
import plotly.graph_objects as go
from data_analysis.data_layer import DataFetcher
from data_analysis.plotter import create_bar_plot, create_line_plot, create_heatmap


# Instantiate the DataFetcher
fetcher = DataFetcher()

def register_callbacks(app):

    @app.callback(
        [Output('graph', 'figure'),
         Output('line-plot', 'figure'),
         Output('heatmap', 'figure')],
        [Input('year-dropdown', 'value'),
         Input('month-dropdown', 'value'),
         Input('day-dropdown', 'value'),
         Input('parameter-dropdown', 'value'),
         Input('building-dropdown', 'value')]
    )
    def update_graphs(year, month, day, parameter, building_name):
        # Map building and parameter to source name and datetime column
        source_mapping = {
            'SM': {'Power': 'SM_Power', 'Voltage': 'SM_Voltage'},
            'CSA': {'Power': 'CSA_Power', 'Voltage': 'CSA_Voltage'},
            'DESE': {'Power': 'DESE_Power', 'Voltage': 'DESE_Voltage'}
        }
        
        # Determine data source and datetime column based on selected building and parameter
        source_name = source_mapping.get(building_name, {}).get(parameter.split()[1])
        datetime_column = f"{building_name}_A_datetime"

        # Asynchronously fetch and preprocess the data
        data = asyncio.run(fetcher.fetch_and_process(source_name, datetime_column))
        
        if data is None:
            # Return empty figures if data fetching failed
            return go.Figure(), go.Figure(), go.Figure()

        # Filter data by selected year, month, and day
        df_filtered = data[
            (data.index.year == year) & 
            (data.index.month == month) & 
            (data.index.day == day)
        ]

         # Create figures using the helper functions from plotter.py
        bar_fig = create_bar_plot(df_filtered, parameter)
        line_fig = create_line_plot(df_filtered, parameter)
        heatmap_fig = create_heatmap(df_filtered, parameter)

        return bar_fig, line_fig, heatmap_fig