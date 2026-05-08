import yfinance as yf
import pandas as pd


def fetch_market(ticker, start_date=None, end_date=None, period=None):
    if period:
        df = yf.download(ticker, period=period, progress=False)
    else:
        df = yf.download(
            ticker,
            start=start_date,
            end=end_date,
            progress=False
        )

    if df is None or df.empty or 'Close' not in df.columns:
        return None

    df = df.reset_index()[['Date', 'Close']]
    df.columns = ['date', 'value']
    df['date'] = pd.to_datetime(df['date'])

    return df
