import yfinance as yf
import pandas as pd

def fetch_sp500():
    df = yf.download('^GSPC', period='2y')

    df = df.reset_index()[['Date', 'Close']]
    df.columns = ['date', 'value']

    # convert to returns
    df['value'] = df['value'].pct_change()
    
    # now convert to volatility signal
    df['value'] = df['value'].rolling(7).std()

    return df.dropna()
    