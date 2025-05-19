import dash
from dash import html, dcc, Output, Input
import requests
from bs4 import BeautifulSoup

app = dash.Dash(__name__)
server = app.server  # for deployment

app.layout = html.Div([
    html.H1("🌤️ Weather Dashboard", style={'textAlign': 'center'}),

    html.Div([
        dcc.Input(id='city-input', type='text', placeholder='e.g. india/mumbai', debounce=True),
        html.Button('Get Weather', id='submit-btn', n_clicks=0)
    ], style={'textAlign': 'center', 'margin': '20px'}),

    html.Div(id='weather-output', style={'textAlign': 'center', 'marginTop': '30px'})
])

@app.callback(
    Output('weather-output', 'children'),
    Input('submit-btn', 'n_clicks'),
    Input('city-input', 'value')
)
def update_weather(n_clicks, city):
    if not city:
        return ""

    city = city.strip().lower()
    url = f"https://www.timeanddate.com/weather/{city}"

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        temperature = soup.find('div', class_='h2').text.strip()
        description = soup.find('div', class_='bk-focus__qlook').find('p').text.strip()

        return html.Div([
            html.H2(f"Weather in {city.title()}"),
            html.P(f"🌡️ Temperature: {temperature}", style={'fontSize': '20px'}),
            html.P(f"🌥️ Condition: {description}", style={'fontSize': '20px'})
        ])

    except:
        return html.Div([
            html.P("City not found or structure changed.", style={'color': 'red'})
        ])

if __name__ == '__main__':
    app.run(debug=True)
