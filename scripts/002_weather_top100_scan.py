from signal_lab.data.sources.markets import get_stock
from signal_lab.pipelines.ingestion import run as ingest
from signal_lab.pipelines.processing import run as process
from signal_lab.pipelines.features import align_signals, add_lags, add_rolling_corr
from signal_lab.analysis.correlation import compute

TOP_100_TICKERS = [
    'AAPL', 'MSFT', 'AMZN', 'GOOGL', 'META',
    'NVDA', 'TSLA', 'BRK-B', 'JPM', 'V',
    'XOM', 'UNH', 'JNJ', 'WMT', 'PG',
    'HD', 'MA', 'BAC', 'CVX', 'ABBV',
]

def run():
    # first get weather
    data = ingest(include=['weather'])
    weather_signals = process({'weather': data['weather']})
    
    results = []
    
    # now get stocks
    for ticker in TOP_100_TICKERS:
        stock_data = get_stock(ticker)
        
        if stock_data is None or stock_data.empty:
            print(f'Skipping {ticker}')
            continue  
            
        stock_signals = process({'stock': stock_data})
        
        # extract Signal objects (NOT dict indexing)
        weather_signal = next(s for s in weather_signals if s.name == 'weather')
        stock_signal = next(s for s in stock_signals if s.name == 'stock')
        
        df = align_signals([weather_signal, stock_signal])

        df = add_lags(df)
        df = add_rolling_corr(df, 'weather', 'stock')
        
        corr = compute(df, 'stock', 'weather')

        results.append({
            'ticker': ticker,
            'corr': corr
        })

    results = sorted(
        results,
        key=lambda x: abs(x['corr']),
        reverse=True
    )
    
    print(results)

if __name__ == '__main__':
    run()