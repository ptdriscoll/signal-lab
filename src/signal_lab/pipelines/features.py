import pandas as pd

def align_signals(data_dict):
    """Aligns datasets into synchronized DataFrame indexed by date, dropping missing values."""
    df = pd.DataFrame()

    for name, d in data_dict.items():
        temp = d.copy()
        temp['date'] = pd.to_datetime(temp['date'])
        temp = temp.set_index('date')
        df[name] = temp['value']

    return df.dropna()

def drop_complete_cases(df, columns=None):
    """Drops rows with NaN is specified column or list of columns, defaulting to all columns."""
    columns = columns or df.columns
    return df.dropna(subset=columns) 

def to_mean_deviation(df, column='value'):
    """Gets each row's deviation from mean."""
    df = df.copy()
    df[column] = df[column] - df[column].mean()
    return df
    
def to_seasonal_mean_deviation(df, column='value', date_col='date', group='month'):
    """Subtracts local seasonal average from a column instead of a global average."""
    df = df.copy()
    
    # ensure dates are in correct format and extract calendar month
    df[date_col] = pd.to_datetime(df[date_col])
    df['_temp_month'] = df[date_col].dt.month
    
    # subtract monthly average from target column
    df[column] = df[column] - df.groupby('_temp_month')[column].transform('mean')
    
    # drop temporary column before returning
    return df.drop(columns=['_temp_month'])    

def to_extreme_signal(df, column='value', threshold='std'):
    """Uses 0 and 1 to flag whether each row is outside deviation.""" 
    df = df.copy()

    if threshold == 'std':
        limit = df[column].std()
    else:
        limit = threshold

    df[column] = (df[column].abs() > limit).astype(int)
    return df

def to_returns(df, column='value'):
    """Gets percentage change between consecutive rows, dropping first row."""
    df = df.copy()
    df[column] = df[column].pct_change()
    return df.dropna()

def to_rolling_volatility(df, column='value', window=7):
    """Gets rolling standard deviation for each window, dropping initial rows."""
    df = df.copy()
    df[column] = df[column].rolling(window).std()
    return df.dropna()

def add_lags(df, columns=None, lags=(1, 2)):
    """
    Generates historical lag features by shifting time-series columns downward.

    Example Output
    --------------                   
    Date     price      price_lag_1  price_lag_2                     
    Day 1    100          NaN          NaN
    Day 2    105        100.0          NaN
    Day 3    102        105.0        100.0
    Day 4    108        102.0        105.0
    """
    df = df.copy()

    columns = columns or df.columns

    for col in columns:
        for lag in lags:
            df[f'{col}_lag_{lag}'] = df[col].shift(lag)

    return df

def add_rolling_corr(df, col_a, col_b, window=30):
    """
    Calculates the rolling Pearson correlation coefficient between two columns.
    
    Example Output
    -------------- 
    Date    col_a  col_b    rolling_corr    Evaluation                                   
    Day 1   50     5000       NaN           Insufficient data (needs 3 rows).
    Day 2   52     5010       NaN           Insufficient data (needs 3 rows).
    Day 3   55     5030      1.00           Days 1-3: Both metrics climbing in tandem.
    Day 4   58     4990     -0.27           Days 2-4: Day 1 dropped. Paths have diverged.
    Day 5   54     4950      0.98           Days 3-5: Both metrics dropped sharply together.
    """
    df = df.copy()

    df['rolling_corr'] = (
        df[col_a]
        .rolling(window)
        .corr(df[col_b])
    )

    return df
