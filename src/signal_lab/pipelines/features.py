import pandas as pd

def align_signals(signals):
    dfs = [s.to_frame() for s in signals]

    df = pd.concat(dfs)
    df = df.pivot(index='date', columns='signal', values='value')

    return df.dropna()

def add_lags(df):
    df = df.copy()

    df['sp500_lag_1'] = df['sp500'].shift(1)
    df['weather_lag_1'] = df['weather'].shift(1)

    df['sp500_lag_2'] = df['sp500'].shift(2)
    df['weather_lag_2'] = df['weather'].shift(2)

    return df
    
def add_rolling_corr(df, window=30):
    df = df.copy()

    df['rolling_corr'] = (
        df['sp500']
        .rolling(window)
        .corr(df['weather'])
    )

    return df    
