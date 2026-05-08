from signal_lab.data.sources.markets import fetch_market
from signal_lab.data.sources.weather import fetch_weather


def run(config):
    data = {}

    for name, params in config.items():

        if name == 'weather':
            data[name] = fetch_weather(**params)

        if name == 'market':
            data[name] = fetch_market(**params)

    return data
