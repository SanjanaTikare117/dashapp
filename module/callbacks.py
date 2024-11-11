from dash import Input, Output
from module.data_processing import preprocess_dataframe, combined_df

def register_callbacks(app):
    @app.callback(
        [Output('year-dropdown', 'options'),
         Output('year-dropdown', 'value'),
         Output('month-dropdown', 'options'),
         Output('month-dropdown', 'value'),
         Output('day-dropdown', 'options'),
         Output('day-dropdown', 'value')],
        [Input('building-dropdown', 'value'),
         Input('parameter-dropdown', 'value')]
    )
    def update_dropdowns(building_name, parameter):
        df_filtered = combined_df.copy()  # Placeholder for building filtering
        year_options = [{'label': str(year), 'value': year} for year in df_filtered.index.year.unique()]
        month_options = [{'label': month, 'value': month} for month in df_filtered.index.month_name().unique()]
        day_options = [{'label': str(day), 'value': day} for day in df_filtered.index.day.unique()]
        return year_options, year_options[0]['value'], month_options, month_options[0]['value'], day_options, day_options[0]['value']

    @app.callback(
        [Output('bar-plot', 'figure'),
         Output('line-plot', 'figure'),
         Output('heatmap', 'figure')],
        [Input('year-dropdown', 'value'),
         Input('month-dropdown', 'value'),
         Input('day-dropdown', 'value'),
         Input('parameter-dropdown', 'value')]
    )
    def update_graphs(year, month, day, parameter):
        # Add graph update logic based on the filtered data
        pass
