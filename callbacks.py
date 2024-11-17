import dash
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import asyncio
from data_analysis.data_layer import DataFetcher  # Ensure you import DataFetcher

# Create an instance of DataFetcher
data_fetcher = DataFetcher()

def register_callbacks(app, fetcher):
    # Callback to update the graphs based on dropdown selection
    @app.callback(
        [Output('bar-graph', 'figure'),
        Output('line-graph', 'figure'),
        Output('heatmap-graph', 'figure')],
        [Input('year-dropdown', 'value'),
        Input('month-dropdown', 'value'),
        Input('day-dropdown', 'value'),
        Input('parameter-dropdown', 'value'),
        Input('building-dropdown', 'value')]
    )
    async def update_graphs(year, month, day, parameter, building_name):
        # Print statement to check callback execution
        print(f"Callback triggered with parameters: {year}, {month}, {day}, {parameter}, {building_name}")
        
        # Create empty figures for bar and line graphs
        bar_fig = go.Figure()
        line_fig = go.Figure()

        # Fetch heatmap data asynchronously
        heatmap_data = await fetcher.fetch_heatmap_data(building_name)
        
        # Debugging output for heatmap data
        print("Fetched heatmap data:")
        print(heatmap_data)

        # If heatmap data is fetched successfully
        if heatmap_data is not None:
            print("Heatmap data retrieved successfully.")

            # Define ordered months and custom labels
            ordered_months = [8, 9, 10, 11, 12] + list(range(1, 8))
            tick_positions = list(range(len(ordered_months)))  # Match position count with number of months
            custom_labels = ['Aug-23', 'Sep-23', 'Oct-23', 'Nov-23', 'Dec-23', 
                            'Jan-24', 'Feb-24', 'Mar-24', 'Apr-24', 'May-24', 'Jun-24', 'Jul-24']

            # Ensure heatmap_data is a 2D array (list of lists)
            if isinstance(heatmap_data, list) and all(isinstance(i, list) for i in heatmap_data):
                fig_heatmap = go.Figure(data=go.Heatmap(
                    z=heatmap_data,
                    colorscale='YlGnBu',
                    colorbar=dict(title='Active Power (W)')
                ))

                # Adjust layout to display the heatmap
                fig_heatmap.update_layout(
                    title='Hourly Power Usage (Normalized) Heatmap',
                    xaxis_title='Date',
                    yaxis_title='Hour',
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    height=700,
                    width=1200,
                    margin=dict(l=50, r=50, t=50, b=100),
                    xaxis=dict(
                        tickvals=tick_positions,
                        ticktext=custom_labels,
                        tickangle=45,
                        tickmode='array',
                        ticklen=5,
                    ),
                    yaxis=dict(
                        tickangle=0,
                        tickvals=list(range(len(heatmap_data))),
                        ticktext=[f"Hour {i}" for i in range(len(heatmap_data))],
                    ),
                    autosize=False
                )
            else:
                fig_heatmap = go.Figure()
                fig_heatmap.update_layout(
                    title='No Data Available for Selected Filters',
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
        else:
            fig_heatmap = go.Figure()
            fig_heatmap.update_layout(
                title='No Data Available for Selected Filters',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )

        return bar_fig, line_fig, fig_heatmap