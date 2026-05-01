from signal_lab.data.sources.markets import fetch_sp500
from signal_lab.data.sources.weather import fetch_weather

def run(include=None):
    include = include or ['sp500', 'weather']

    data = {}

    if 'sp500' in include:
        data['sp500'] = fetch_sp500()

    if 'weather' in include:
        data['weather'] = fetch_weather()

    return data
    