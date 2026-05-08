import pandas as pd


def align_signals(data_dict):
    df = pd.DataFrame()

    for name, d in data_dict.items():
        temp = d.copy()
        temp['date'] = pd.to_datetime(temp['date'])
        temp = temp.set_index('date')
        df[name] = temp['value']

    return df.dropna()


def drop_complete_cases(df, columns=None):
    columns = columns or df.columns
    return df.dropna(subset=columns)

def to_mean_deviation(df, column='value'):
    df = df.copy()
    df[column] = df[column] - df[column].mean()
    return df

def to_extreme_signal(df, column='value', threshold='std'):
    df = df.copy()

    if threshold == 'std':
        limit = df[column].std()
    else:
        limit = threshold

    df[column] = (df[column].abs() > limit).astype(int)
    return df

def to_returns(df, column='value'):
    df = df.copy()
    df[column] = df[column].pct_change()
    return df.dropna()


def to_rolling_volatility(df, column='value', window=7):
    df = df.copy()
    df[column] = df[column].rolling(window).std()
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
