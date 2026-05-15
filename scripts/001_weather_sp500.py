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

rolling_title='Rolling Correlation: Weather vs SP500'
rolling_plot_path = f'{output_dir}/rolling_corr.png'
rolling_csv_path = f'{output_dir}/rolling_corr.csv'

event_title = 'Market Response Around Weather Extremes'
event_plot_path = f'{output_dir}/weather_extremes.png'
event_csv_path = f'{output_dir}/weather_extremes.csv'

plot_rolling_corr(df, title=rolling_title, save_path=rolling_plot_path, csv_path=rolling_csv_path)
plot_event_study(df, title=event_title, save_path=event_plot_path, csv_path=event_csv_path)
