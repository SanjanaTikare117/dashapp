from flask import Flask, render_template
from dash import Dash
from templates.layouts import create_layout
from module.callbacks import register_callbacks
from data_analysis.data_layer import DataFetcher  # Import DataFetcher
from module.callbacks import register_callbacks
# Initialize Flask server
server = Flask(__name__)

# Initialize Dash app and attach to Flask server
app = Dash(__name__, server=server)
app.layout = create_layout()

# Initialize DataFetcher and register callbacks
fetcher = DataFetcher()
register_callbacks(app, fetcher)  # Pass fetcher to register_callbacks

@server.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    server.run(debug=True, port=5000)
