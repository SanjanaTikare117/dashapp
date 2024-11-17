import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import numpy as np

# Generate dummy data for testing
def generate_dummy_data():
    date_range = pd.date_range(start='2023-01-01', end='2023-12-31', freq='H')
    df = pd.DataFrame({
        'datetime': date_range,
        'Total Active Power': np.random.uniform(100, 500, len(date_range)),
        'Total Voltage': np.random.uniform(220, 240, len(date_range))
    })
    return df

df = generate_dummy_data()
# df = get_csa_power_data()

# Preprocess the dataframes
def preprocess_dataframe(df, value_column):
    df['datetime'] = pd.to_datetime(df['datetime'])  # Ensure datetime column is in datetime format
    df.set_index('datetime', inplace=True)
    numeric_cols = df.select_dtypes(include=['number']).columns
    df_hourly = df[numeric_cols].resample('h').mean()
    daily_data = df[numeric_cols].resample('D').agg({
        value_column: ['min', 'max', 'mean']
    })
    daily_data.columns = ['min', 'max', 'mean']
    daily_data = daily_data.reset_index()
    return df, daily_data

# Preprocess the dummy data
combined_df, combined_daily_data = preprocess_dataframe(df, 'Total Active Power')

# Initialize the app
app = Dash(__name__)

# App layout with enhanced UI
app.layout = html.Div(
    style={
        'backgroundImage': 'url(https://images.fineartamerica.com/images/artworkimages/mediumlarge/1/indian-institute-of-science-main-building-nitesh-bhatia.jpg)',  # Path to your background image
        'backgroundSize': 'cover',
        'padding': '20px',
        'height': '100vh',
        'overflow': 'hidden',
        'display': 'flex',
        'flexDirection': 'column',
        'border': '5px solid #9400D3',  # Neon purple border around the whole dashboard
        'borderRadius': '10px'
    },
    children=[
        # Title Box
        html.Div(
            style={
                'textAlign': 'center',
                'color': '#9400D3',  # Neon purple text
                'fontSize': '32px',
                'fontWeight': 'bold',
                'marginBottom': '20px',
                'border': '2px solid #9400D3',  # Neon purple border for the title box
                'borderRadius': '10px',
                'padding': '10px',
                'backgroundColor': '#9DF1DF'  # White background for the title box
            },
            children="IISc Energy Dashboard"
        ),

        # Main content area
        html.Div(
            style={
                'display': 'flex',
                'flexDirection': 'row',
                'justifyContent': 'space-between',
                'flex': '1'
            },
            children=[
                # Sidebar for dropdowns and controls
                html.Div(
                    style={
                        'flex': '0.7',  # Reduced width for dropdown area
                        'padding': '20px',
                        'borderRadius': '10px',
                        'color': '#9400D3',  # Neon purple text
                        'marginRight': '10px',
                        'display': 'flex',
                        'flexDirection': 'column',
                        'justifyContent': 'flex-start',
                        'height': '90vh',
                        'border': '1px solid #9400D3'  # Neon purple border only
                    },
                    children=[
                        html.Label('Building Name', style={'color': '#9400D3', 'fontWeight': 'bold'}),
                        dcc.Dropdown(
                            options=[
                                {'label': 'SM', 'value': 'SM'},
                                {'label': 'Dese', 'value': 'Dese'},
                                {'label': 'Csa', 'value': 'Csa'}
                            ],
                            value='SM',
                            id='building-dropdown',
                            style={
                                'backgroundColor': '1px solid #FFF1DB',  # White background for dropdown
                                'color': '#0F6292',  # Neon purple text
                                'border': '1px solid #9400D3'  # Neon purple border
                            }
                        ),
                        
                        html.Br(),
                        html.Label('Parameters', style={'color': '#9400D3', 'fontWeight': 'bold'}),
                        dcc.Dropdown(
                            options=[
                                {'label': 'Total Active Power', 'value': 'Total Active Power'},
                                {'label': 'Total Voltage', 'value': 'Total Voltage'}
                            ],
                            value='Total Active Power',
                            id='parameter-dropdown',
                            style={
                                'backgroundColor': '1px solid #FFF1DB',  # White background for dropdown
                                'color': '#0F6292',  # Neon purple text
                                'border': '1px solid #9400D3'  # Neon purple border
                            }
                        ),

                        html.Br(),
                        html.Label('Year', style={'color': '#9400D3', 'fontWeight': 'bold'}),
                        dcc.Dropdown(
                            id='year-dropdown',
                            style={
                                'backgroundColor': '1px solid #FFF1DB',  # White background for dropdown
                                'color': '#0F6292',  # Neon purple text
                                'border': '1px solid #9400D3'  # Neon purple border
                            }
                        ),

                        html.Br(),
                        html.Label('Month', style={'color': '#9400D3', 'fontWeight': 'bold'}),
                        dcc.Dropdown(
                            id='month-dropdown',
                            style={
                                'backgroundColor': '1px solid #FFF1DB',  # White background for dropdown
                                'color': '#0F6292',  # Neon purple text
                                'border': '1px solid #9400D3'  # Neon purple border
                            }
                        ),

                        html.Br(),
                        html.Label('Day', style={'color': '#9400D3', 'fontWeight': 'bold'}),
                        dcc.Dropdown(
                            id='day-dropdown',
                            style={
                                'backgroundColor': '1px solid #FFF1DB',  # White background for dropdown
                                'color': '#0F6292',  # Neon purple text
                                'border': '1px solid #9400D3'  # Neon purple border
                            }
                        ),
                    ]
                ),

                # Graph area
                html.Div(
                    style={
                        'flex': '3',
                        'display': 'flex',
                        'flexDirection': 'column',
                        'justifyContent': 'space-between',
                        'height': '100vh',
                        'padding': '10px',
                    },
                    children=[
                        # Bar and Line Plots side-by-side
                        html.Div(
                            style={
                                'display': 'flex',
                                'flexDirection': 'row',
                                'justifyContent': 'space-between',
                                'flex': '1',
                                'marginBottom': '10px',
                            },
                            children=[
                                html.Div(
                                    style={
                                        'flex': '1',
                                        'border': '1px solid #9400D3',
                                        'borderRadius': '10px',
                                        'marginRight': '5px',
                                        'padding': '10px',
                                        #'backgroundColor': '#B5CFB7',  # Updated background color
                                    },
                                    children=[
                                        dcc.Graph(id='bar-plot', style={'height': '100%', 'width': '100%'})
                                    ]
                                ),
                                html.Div(
                                    style={
                                        'flex': '1',
                                        'border': '1px solid #9400D3',
                                        'borderRadius': '10px',
                                        'marginLeft': '5px',
                                        'padding': '10px',
                                        #'backgroundColor': '#B5CFB7',  # Updated background color
                                    },
                                    children=[
                                        dcc.Graph(id='line-plot', style={'height': '100%', 'width': '100%'})
                                    ]
                                ),
                            ]
                        ),

                        # Heatmap at the bottom
                        html.Div(
                            style={
                                'flex': '1',
                                'border': '1px solid #9400D3',
                                'borderRadius': '10px',
                                'padding': '10px',
                                #'backgroundColor': '#B5CFB7',  # Updated background color
                            },
                            children=[
                                dcc.Graph(id='heatmap', style={'height': '100%', 'width': '100%'})
                            ]
                        ),
                    ]
                ),
            ]
        ),
    ]
)

# Update dataset dropdown options based on building name and parameter
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
    # Filter the data based on the selected building name
    df_filtered = combined_df.copy()  # Placeholder for building name filtering
    
    # Update year, month, and day options
    year_options = [{'label': str(year), 'value': year} for year in df_filtered.index.year.unique()]
    month_options = [{'label': month, 'value': month} for month in df_filtered.index.month_name().unique()]
    day_options = [{'label': str(day), 'value': day} for day in df_filtered.index.day.unique()]
    
    return year_options, year_options[0]['value'], month_options, month_options[0]['value'], day_options, day_options[0]['value']

# Update bar, line plots, and heatmap based on dropdown selections
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
    # Filter data based on selected year, month, and day
    df_filtered = combined_df.copy()
    if year:
        df_filtered = df_filtered[df_filtered.index.year == year]
    if month:
        df_filtered = df_filtered[df_filtered.index.month == pd.to_datetime(month, format='%B').month]
    if day:
        df_filtered = df_filtered[df_filtered.index.day == int(day)]

    # Bar Plot
    bar_fig = px.bar(df_filtered, x=df_filtered.index, y=parameter, title=f'{parameter} Bar Plot')
    bar_fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title={'font': {'color': '#0F6292'}},
        xaxis_title={'font': {'color': '#0F6292'}},
        yaxis_title={'font': {'color': '#0F6292'}}
    )

    # Line Plot
    line_fig = px.line(df_filtered, x=df_filtered.index, y=parameter, title=f'{parameter} Line Plot')
    line_fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title={'font': {'color': '#0F6292'}},
        xaxis_title={'font': {'color': '#0F6292'}},
        yaxis_title={'font': {'color': '#0F6292'}}
    )

    # Heatmap
    if month:
        df_filtered_month = df_filtered[df_filtered.index.month == pd.to_datetime(month, format='%B').month]
        df_hourly = df_filtered_month.resample('H').mean()
        df_hourly['normalized_power'] = (df_hourly[parameter] - df_hourly[parameter].min()) / (df_hourly[parameter].max() - df_hourly[parameter].min())
        heatmap_df = df_hourly.pivot_table(index=df_hourly.index.hour, columns=df_hourly.index.date, values='normalized_power')
        fig_heatmap = go.Figure(data=go.Heatmap(z=heatmap_df.values, x=heatmap_df.columns, y=heatmap_df.index, colorscale='Viridis'))
        fig_heatmap.update_layout(
            title='Hourly Power Usage (Normalized) Heatmap',
            xaxis_title='Date',
            yaxis_title='Hour',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
    else:
        fig_heatmap = go.Figure()  # Empty heatmap if no month is selected

    return bar_fig, line_fig, fig_heatmap

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True,port=8099)
