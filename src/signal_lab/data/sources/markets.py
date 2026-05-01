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

def get_stock(ticker: str):
    df = yf.download(ticker, progress=False)

    # check whether empty or invalid
    if df is None or df.empty or 'Close' not in df.columns:
        return None

    df = df[['Close']].copy()
    df['value'] = df['Close'].pct_change()
    
    df = df[['value']].dropna()
    df.index = pd.to_datetime(df.index)

    df = df.reset_index()
    df.columns = ['date', 'value']

    return df
    