# data/sources/weather.py

import requests
import pandas as pd

def fetch_weather():
    url = 'https://archive-api.open-meteo.com/v1/archive'

    params = {
        'latitude': 40.71,   # New York
        'longitude': -74.01,
        'start_date': '2023-01-01',
        'end_date': '2024-12-31',
        'daily': 'temperature_2m_mean',
        'timezone': 'UTC'
    }

    res = requests.get(url, params=params).json()

    df = pd.DataFrame({
        'date': res['daily']['time'],
        'value': res['daily']['temperature_2m_mean']
    })

    # simple deviation (baseline = mean)
    df['value'] = df['value'] - df['value'].mean()
    
    # now convert to extreme event signal
    df['value'] = (df['value'].abs() > df['value'].std()).astype(int)

    return df
    