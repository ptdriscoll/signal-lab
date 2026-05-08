from signal_lab.pipelines.ingestion import run as ingest
from signal_lab.data.sources.markets import fetch_market
from signal_lab.pipelines.processing import run as process
from signal_lab.analysis.correlation import compute
from signal_lab.config.exp_002_weather_top100_scan import DATA, MARKET, TOP_TICKERS
import os
import pandas as pd
from signal_lab.pipelines.features import (
    align_signals,
    add_lags,
    add_rolling_corr,
    to_returns
)

def run():
    weather_signals = ingest(DATA)
    weather = weather_signals['weather']

    results = []
    for ticker in TOP_TICKERS:
        stock = fetch_market(
            ticker=ticker,
            start_date=MARKET['start_date'],
            end_date=MARKET['end_date']
        )

        if stock is None or stock.empty:
            print(f'Skipping {ticker}')
            continue

        stock_returns = to_returns(stock)

        df = align_signals({
            'weather': weather,
            'stock': stock_returns
        })

        df = add_lags(df)
        df = add_rolling_corr(df, 'weather', 'stock')
        corr = compute(df, 'weather', 'stock')
        corr = float(corr)

        results.append({
            'ticker': ticker,
            'corr': corr
        })

    results.sort(key=lambda x: abs(x['corr']), reverse=True)
    for i, r in enumerate(results[:10], 1):
        print(f"{i:02d}. {r['ticker']:6} {r['corr']:.4f}")

    output_dir = 'outputs/002_weather_top100_scan'
    os.makedirs(output_dir, exist_ok=True)    
    pd.DataFrame(results).to_csv(
        f'{output_dir}/results.csv',
        index=False
    )    

if __name__ == '__main__':
    run()
