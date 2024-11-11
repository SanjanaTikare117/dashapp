from dash import dcc, html

def create_layout(app):
    layout = html.Div(
        style={
            'backgroundImage': 'url(https://images.fineartamerica.com/images/artworkimages/mediumlarge/1/indian-institute-of-science-main-building-nitesh-bhatia.jpg)', 
            'backgroundSize': 'cover',
            'padding': '20px',
            'height': '100vh',
            'overflow': 'hidden',
            'display': 'flex',
            'flexDirection': 'column',
            'border': '5px solid #9400D3',  
            'borderRadius': '10px'
        },
        children=[
            html.Div(
                style={
                    'textAlign': 'center',
                    'color': '#9400D3',
                    'fontSize': '32px',
                    'fontWeight': 'bold',
                    'marginBottom': '20px',
                    'border': '2px solid #9400D3',
                    'borderRadius': '10px',
                    'padding': '10px',
                    'backgroundColor': '#9DF1DF'
                },
                children="IISc Energy Dashboard"
            ),
            # Add remaining layout content...
        ]
    )
    return layout
