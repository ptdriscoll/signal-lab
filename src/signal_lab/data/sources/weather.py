import requests
import pandas as pd


def fetch_weather(lat, lon, start_date, end_date):
    url = 'https://archive-api.open-meteo.com/v1/archive'

    params = {
        'latitude': lat,
        'longitude': lon,
        'start_date': start_date,
        'end_date': end_date,
        'daily': 'temperature_2m_mean',
        'timezone': 'UTC'
    }

    res = requests.get(url, params=params).json()

    return pd.DataFrame({
        'date': pd.to_datetime(res['daily']['time']),
        'value': res['daily']['temperature_2m_mean']
    })
