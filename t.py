# Import the Dash app from the 'modules/dash.py' file
from module.dash import app

if __name__ == '__main__':
    app.run_server(debug=True)
