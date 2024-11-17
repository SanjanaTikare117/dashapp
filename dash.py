import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd
from data_analysis.data_layer import DataFetcher
import asyncio

# Initialize Dash app
app = dash.Dash(__name__)

# Initialize DataFetcher
data_fetcher = DataFetcher()

# Layout of the Dash app with inline CSS
app.layout = html.Div(
    style={"backgroundColor": "#B5CFB7", "display": "flex", "height": "100vh"},
    children=[
        # Sidebar for dropdowns
        html.Div(
            style={
                "width": "250px", "backgroundColor": "#fff", "padding": "20px",
                "borderRight": "2px solid #ddd", "position": "relative"
            },
            children=[
                html.H2("Indian Institute of Science", style={
                    "textAlign": "center", "color": "#333", "fontSize": "22px", "fontWeight": "bold"
                }),

                # Type Dropdown (Year, Month, or Day)
                html.Label("Select Type", style={"fontSize": "16px", "fontWeight": "bold"}),
                dcc.Dropdown(
                    id="type-dropdown",
                    options=[
                        {"label": "Year", "value": "year"},
                        {"label": "Month", "value": "month"},
                        {"label": "Day", "value": "day"}
                    ],
                    value="year",  # Default to Month
                    style={"width": "100%", "backgroundColor": "#fff", "fontSize": "16px", "borderRadius": "5px"}
                ),
                html.Br(),

                # Year Dropdown (Always visible)
                html.Label("Select Year", style={"fontSize": "16px", "fontWeight": "bold"}),
                dcc.Dropdown(
                    id="year-dropdown",
                    options=[
                        {"label": "2023", "value": "2023"},
                        {"label": "2024", "value": "2024"}
                    ],
                    value="2023",  # Default to 2023
                    style={"width": "100%", "backgroundColor": "#fff", "fontSize": "16px", "borderRadius": "5px"}
                ),
                html.Br(),

                # Month Dropdown (Initially visible when Type is Month or Day)
                html.Div(
                    id="month-dropdown-container",
                    children=[
                        html.Label("Select Month", style={"fontSize": "16px", "fontWeight": "bold"}),
                        dcc.Dropdown(
                            id="month-dropdown",
                            options=[
                                {"label": "January", "value": "January"},
                                {"label": "February", "value": "February"},
                                {"label": "March", "value": "March"},
                                {"label": "April", "value": "April"},
                                {"label": "May", "value": "May"},
                                {"label": "June", "value": "June"},
                                {"label": "July", "value": "July"},
                                {"label": "August", "value": "August"},
                                {"label": "September", "value": "September"},
                                {"label": "October", "value": "October"},
                                {"label": "November", "value": "November"},
                                {"label": "December", "value": "December"},
                            ],
                            #value="January",  # Default to January
                            style={"width": "100%", "backgroundColor": "#fff", "fontSize": "16px", "borderRadius": "5px"}
                        ),
                    ]
                ),
                html.Div(
                    id="day-dropdown-container",
                    style={"display": "none"},
                    children=[
                        html.Label("Select Day", style={"fontSize": "16px", "fontWeight": "bold"}),
                        dcc.Dropdown(
                            id="day-dropdown",
                            options=[
                                {"label": "Monday", "value": "Monday"},
                                {"label": "Tuesday", "value": "Tuesday"},
                                {"label": "Wednesday", "value": "Wednesday"},
                                {"label": "Thursday", "value": "Thursday"},
                                {"label": "Friday", "value": "Friday"},
                                {"label": "Saturday", "value": "Saturday"},
                                {"label": "Sunday", "value": "Sunday"},
                            ],
                            #value="Monday",  # Default to Monday
                            style={"width": "100%", "backgroundColor": "#fff", "fontSize": "16px", "borderRadius": "5px"}
                        ),
                    ]
                ),
                html.Br(),

                # Building name dropdown
                html.Label("Building", style={"fontSize": "16px", "fontWeight": "bold"}),
                dcc.Dropdown(
                    id="building-dropdown",
                    options=[{"label": building, "value": building} for building in ["SM", "DESE", "CSA"]],
                    value="SM",  # Default to SM
                    style={"width": "100%", "backgroundColor": "#fff", "fontSize": "16px", "borderRadius": "5px"}
                ),
                html.Br(),

                # Parameter dropdown (Total Active Power or Total Voltage)
                html.Label("Parameter", style={"fontSize": "16px", "fontWeight": "bold"}),
                dcc.Dropdown(
                    id="parameter-dropdown",
                    options=[{"label": "Total Active Power", "value": "Power"},
                             {"label": "Total Voltage", "value": "Voltage"}],
                    value="Power",  # Default to Total Active Power
                    style={"width": "100%", "backgroundColor": "#fff", "fontSize": "16px", "borderRadius": "5px"}
                ),
                html.Br(),

                # Graph type dropdown (Line, Bar, Heatmap)
                html.Label("Graph Type", style={"fontSize": "16px", "fontWeight": "bold"}),
                dcc.Dropdown(
                    id="graph-type-dropdown",
                    options=[{"label": "Line Plot", "value": "line"},
                             {"label": "Bar Plot", "value": "bar"},
                             {"label": "Heatmap", "value": "heatmap"}],
                    value="line",  # Default to Line Plot
                    style={"width": "100%", "backgroundColor": "#fff", "fontSize": "16px", "borderRadius": "5px"}
                )
            ]
        ),
        
        # Graph area (right side)
        html.Div(
            style={"flex": 1, "padding": "20px", "overflowY": "auto"},
            children=[dcc.Graph(id="main-graph", style={"height": "80vh"})]
        )
    ]
)

# Function to run asynchronous task synchronously
def get_data_sync(source_name, datetime_name):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    data = loop.run_until_complete(data_fetcher.fetch_and_process(source_name, datetime_name))
    return data

# Callback to update visibility of Month, Day, and Year dropdowns based on the selected Type
@app.callback(
    [
        Output("month-dropdown-container", "style"),
        Output("day-dropdown-container", "style"),
        Output("year-dropdown", "style")
    ],
    Input("type-dropdown", "value")
)
def update_dropdown_visibility(type_value):
    if type_value == "year":
        return {"display": "none"}, {"display": "none"}, {"display": "block"}
    elif type_value == "month":
        return {"display": "block"}, {"display": "none"}, {"display": "block"}
    elif type_value == "day":
        return {"display": "block"}, {"display": "block"}, {"display": "block"}

# Callback to update the graph based on the dropdown selections
@app.callback(
    Output("main-graph", "figure"),
    [
        Input("year-dropdown", "value"),
        Input("month-dropdown", "value"),
        Input("day-dropdown", "value"),
        Input("building-dropdown", "value"),
        Input("parameter-dropdown", "value"),
        Input("graph-type-dropdown", "value")
    ]
)
def update_graph(selected_year, selected_month, selected_day, building, parameter, graph_type):
    source_name = f"{building}_{parameter}"
    datetime_name = f"{building}_A_datetime" if parameter == "Power" else f"{building}_A_Voltage_datetime"

    data = get_data_sync(source_name, datetime_name)

    if data is not None:
        print(selected_day)
        print(selected_month)
        print(selected_year)
        # Filter data based on selected year, month, or day
        if selected_year:
            filtered_data = data[data.index.year == int(selected_year)]
        if selected_month:
            filtered_data = data[data.index.month_name() == selected_month]
        if selected_day:
            filtered_data = data[data.index.day_name() == selected_day]

        print(filtered_data.head())

        # Create the graph based on the selected graph type
        if graph_type == "line":
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=filtered_data.index, y=filtered_data["Total Active Power"], mode="lines"))
        elif graph_type == "bar":
            fig = go.Figure()
            fig.add_trace(go.Bar(x=filtered_data.index, y=filtered_data["Total Active Power"]))
        elif graph_type == "heatmap":
            fig = go.Figure(data=go.Heatmap(
                z=filtered_data.pivot_table(index="Hour", columns="Day", values="Total Active Power").values
            ))
        return fig

    return go.Figure()

if __name__ == "__main__":
    app.run_server(debug=True)
