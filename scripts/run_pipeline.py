from signal_lab.pipelines.ingestion import run as ingest
from signal_lab.pipelines.processing import run as process
from signal_lab.pipelines.features import align_signals, add_lags, add_rolling_corr
from signal_lab.analysis.correlation import compute
from signal_lab.analysis.plots import plot_rolling_corr, plot_event_study

data = ingest()
signals = process(data)
df = align_signals(signals)
df = add_lags(df)
df = add_rolling_corr(df)

corr = compute(df)
print(corr['sp500'])

plot_rolling_corr(df)
plot_event_study(df)
