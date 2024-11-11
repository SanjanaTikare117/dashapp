from dash import Dash
from module.layout import create_layout
from module.callbacks import register_callbacks

# Initialize the app
app = Dash(__name__)

# Set the layout
app.layout = create_layout(app)

# Register callbacks
register_callbacks(app)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8000)
