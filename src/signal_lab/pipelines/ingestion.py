from signal_lab.data.sources.markets import fetch_sp500
from signal_lab.data.sources.weather import fetch_weather

def run():
    markets = fetch_sp500()
    weather = fetch_weather()

    return {
        'sp500': markets,
        'weather': weather
    }
