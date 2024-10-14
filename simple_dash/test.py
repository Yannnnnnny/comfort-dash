import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import numpy as np
import plotly.graph_objs as go

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Thermal Comfort with Fan Use"),
    
    # Input components for user input (air speed, metabolic rate, clothing level)
    html.Div([
        html.Label("Air Speed (m/s)"),
        dcc.Slider(
            id='air-speed-slider',
            min=0.3, max=4.5, step=0.1, value=0.8,
            marks={i: f'{i:.1f} m/s' for i in np.arange(0.3, 4.6, 0.5)}
        ),
        html.Br(),
        
        html.Label("Metabolic Rate (met)"),
        dcc.Slider(
            id='metabolic-rate-slider',
            min=0.7, max=1.9, step=0.1, value=1.5,
            marks={i: f'{i:.1f} met' for i in np.arange(0.7, 2.0, 0.2)}
        ),
        html.Br(),
        
        html.Label("Clothing Level (clo)"),
        dcc.Slider(
            id='clothing-level-slider',
            min=0.0, max=0.6, step=0.1, value=0.5,
            marks={i: f'{i:.1f} clo' for i in np.arange(0.0, 0.7, 0.1)}
        ),
        html.Br(),
    ]),
    
    # Graph to display the cooling regions and user inputs
    dcc.Graph(id='comfort-graph')
])

# Define the callback to update the graph based on user input
@app.callback(
    Output('comfort-graph', 'figure'),
    [
        Input('air-speed-slider', 'value'),
        Input('metabolic-rate-slider', 'value'),
        Input('clothing-level-slider', 'value')
    ]
)
def update_graph(air_speed, metabolic_rate, clothing_level):
    # Generate a range of temperature and humidity
    temperature = np.linspace(30, 50, 100)
    humidity = np.linspace(5, 85, 100)
    temperature, humidity = np.meshgrid(temperature, humidity)
    
    # Simulate some condition where the fan is beneficial or harmful
    cooling_effect = (air_speed * metabolic_rate / (clothing_level + 1)) * humidity / temperature
    
    # Define the thresholds for beneficial, heat strain, and harmful fan use
    green_zone = (cooling_effect < 0.8)
    dark_green_zone = (cooling_effect >= 0.8) & (cooling_effect < 1.5)
    red_zone = (cooling_effect >= 1.5)
    
    fig = go.Figure()
    
    # Add light green area (no heat strain)
    fig.add_trace(go.Contour(
        x=np.linspace(5, 85, 100), y=np.linspace(30, 50, 100), z=green_zone.astype(int),
        showscale=False, colorscale=[[0, 'lightgreen'], [1, 'lightgreen']],
        name='No Heat Strain', opacity=0.5, contours=dict(start=1, end=1)
    ))
    
    # Add dark green area (heat strain but fans still beneficial)
    fig.add_trace(go.Contour(
        x=np.linspace(5, 85, 100), y=np.linspace(30, 50, 100), z=dark_green_zone.astype(int),
        showscale=False, colorscale=[[0, 'darkgreen'], [1, 'darkgreen']],
        name='Heat Strain, Fan Still Beneficial', opacity=0.5, contours=dict(start=1, end=1)
    ))
    
    # Add red area (heat strain, fans not beneficial)
    fig.add_trace(go.Contour(
        x=np.linspace(5, 85, 100), y=np.linspace(30, 50, 100), z=red_zone.astype(int),
        showscale=False, colorscale=[[0, 'red'], [1, 'red']],
        name='Fans Not Beneficial', opacity=0.5, contours=dict(start=1, end=1)
    ))

    # Customize the layout of the plot
    fig.update_layout(
        title=f'Fan Effectiveness (Air Speed: {air_speed} m/s, Metabolic Rate: {metabolic_rate} met, Clothing: {clothing_level} clo)',
        xaxis_title='Relative Humidity (%)',
        yaxis_title='Operative Temperature (°C)',
        xaxis=dict(range=[5, 85]),
        yaxis=dict(range=[30, 50])
    )
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
