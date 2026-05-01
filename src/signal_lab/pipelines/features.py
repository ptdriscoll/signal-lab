import pandas as pd

def align_signals(signals):
    dfs = [s.to_frame() for s in signals]

    df = pd.concat(dfs)
    df = df.pivot(index='date', columns='signal', values='value')

    return df.dropna()

def add_lags(df, columns=None, lags=(1, 2)):
    df = df.copy()

    columns = columns or df.columns

    for col in columns:
        for lag in lags:
            df[f'{col}_lag_{lag}'] = df[col].shift(lag)

    return df
    
def add_rolling_corr(df, col_a, col_b, window=30):
    df = df.copy()

    df['rolling_corr'] = (
        df[col_a]
        .rolling(window)
        .corr(df[col_b])
    )

    return df  
