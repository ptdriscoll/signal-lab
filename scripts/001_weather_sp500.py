from signal_lab.pipelines.ingestion import run as ingest
from signal_lab.analysis.plots import plot_rolling_corr, plot_event_study
from signal_lab.config.exp_001_weather_sp500 import DATA
import os
from signal_lab.pipelines.features import (
    to_mean_deviation,
    to_extreme_signal,
    to_returns, 
    to_rolling_volatility, 
    align_signals, 
    add_lags, 
    add_rolling_corr
)

data = ingest(DATA)

data['weather'] = to_mean_deviation(data['weather'])
data['weather'] = to_extreme_signal(data['weather'])

data['market'] = to_returns(data['market'])
data['market'] = to_rolling_volatility(data['market'], window=7)

df = align_signals(data)
df = add_lags(df)
df = add_rolling_corr(df, 'market', 'weather')

corr = df.corr()
print(corr['market'])

output_dir = 'outputs/001_weather_sp500'
os.makedirs(output_dir, exist_ok=True)

plot_rolling_corr(df, save_path=f'{output_dir}/rolling_corr.png', title='Rolling Correlation: Weather vs SP500')
plot_event_study(df, save_path=f'{output_dir}/weather_extremes.png', title='Market Response Around Weather Extremes')
