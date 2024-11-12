# layouts/layouts.py
import dash
from dash import dcc, html

def create_layout():
    return html.Div(
        style={'padding': '20px', 
               'height': '100vh', 
               'overflowY': 'auto'},
        children=[
            # Navbar (with IISc in the center)
            html.Nav(
                children=[
                    html.Div(
                        children=[
                            html.Div(
                                children=[
                                    html.A("IISc Energy Dashboard", href="#", style={
                                        'color': 'white',
                                        'fontSize': '24px',
                                        'fontWeight': 'bold',
                                        'textDecoration': 'none',
                                        'padding': '10px',
                                        'display': 'flex',
                                        'justifyContent': 'center',
                                        'width': '100%'
                                    }),
                                ],
                                style={
                                    'backgroundColor': '#004d00',  # IISc green color
                                    'display': 'flex',
                                    'justifyContent': 'center',
                                    'alignItems': 'center',
                                    'padding': '10px',
                                    # 'boxShadow': '0px 4px 8px rgba(0, 0, 0, 0.1)'
                                }
                            )
                        ]
                    ),
                ]
            ),
            
            # Main Content Area
            html.Div(
                style={'padding': '20px', 
                       'height': 'calc(100vh - 60px)', 
                       'overflowY': 'auto'},
                children=[
                    # Sidebar with dropdowns
                    html.Div(
                        style={'display': 'flex', 
                               'flexDirection': 'row', 
                               'flexWrap': 'wrap', 
                               'justifyContent': 'space-between'},
                        children=[
                            # Sidebar
                            html.Div([
                                html.Label('Building Name'),
                                dcc.Dropdown(id='building-dropdown', options=[
                                    {'label': 'SM', 'value': 'SM'},
                                    {'label': 'CSA', 'value': 'CSA'},
                                    {'label': 'DESE', 'value': 'DESE'}
                                ], style={'width': '180px'}),  # Reduced width

                                html.Label('Parameters'),
                                dcc.Dropdown(id='parameter-dropdown', options=[
                                    {'label': 'Total Active Power', 'value': 'Total Active Power'},
                                    {'label': 'Total Voltage', 'value': 'Total Voltage'}
                                ], style={'width': '180px'}),  # Reduced width

                                html.Label('Year'),
                                dcc.Dropdown(id='year-dropdown', options=[
                                    {'label': '2023', 'value': '2023'},
                                    {'label': '2024', 'value': '2024'}
                                ], style={'width': '180px'}),  # Reduced width

                                html.Label('Month'),
                                dcc.Dropdown(id='month-dropdown', options=[
                                    {'label': 'January', 'value': 'January'},
                                    {'label': 'February', 'value': 'February'},
                                    {'label': 'March', 'value': 'March'},
                                    {'label': 'April', 'value': 'April'},
                                    {'label': 'May', 'value': 'May'},
                                    {'label': 'June', 'value': 'June'},
                                    {'label': 'July', 'value': 'July'},
                                    {'label': 'August', 'value': 'August'},
                                    {'label': 'September', 'value': 'September'},
                                    {'label': 'October', 'value': 'October'},
                                    {'label': 'November', 'value': 'November'},
                                    {'label': 'December', 'value': 'December'}
                                ], style={'width': '180px'}),  # Reduced width

                                html.Label('Day'),
                                dcc.Dropdown(id='day-dropdown', options=[
                                    {'label': 'Monday', 'value': 'Monday'},
                                    {'label': 'Tuesday', 'value': 'Tuesday'},
                                    {'label': 'Wednesday', 'value': 'Wednesday'},
                                    {'label': 'Thursday', 'value': 'Thursday'},
                                    {'label': 'Friday', 'value': 'Friday'},
                                    {'label': 'Saturday', 'value': 'Saturday'},
                                    {'label': 'Sunday', 'value': 'Sunday'}
                                ], style={'width': '180px'}),  # Reduced width
                            ], style={'padding': '10px', 'width': '25%', 'boxSizing': 'border-box'}),  # Sidebar width

                            # Graph Section: Two graphs inside one frame (fixed height, non-scrollable)
                            html.Div(
                                style={'width': '70%',
                                       'height': '500px',
                                       'overflow': 'hidden', 
                                       'display': 'flex', 
                                       'flexDirection': 'row', 
                                       'justifyContent': 'space-between'},
                                children=[
                                    # Bar Graph and Line Graph in a fixed, non-scrollable container
                                    html.Div(
                                        style={'width': '48%', 
                                               'height': '100%'},
                                        children=[
                                            dcc.Graph(id='bar-plot', style={'height': '100%'})
                                        ]
                                    ),
                                    html.Div(
                                        style={'width': '48%', 'height': '100%'},
                                        children=[
                                            dcc.Graph(id='line-plot', style={'height': '100%'})
                                        ]
                                    )
                                ]
                            )
                        ]
                    ),

                    # Heatmap Section placed below
                    html.Div(
                        style={'width': '100%', 'paddingTop': '20px'},
                        children=[
                            dcc.Graph(id='heatmap', style={'height': '400px'})
                        ]
                    )
                ]
            )
        ]
    )














































































