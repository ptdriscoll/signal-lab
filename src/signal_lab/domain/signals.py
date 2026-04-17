import pandas as pd

class Signal:
    def __init__(self, name: str, df: pd.DataFrame):
        self.name = name
        self.df = df.copy()

        self._validate()

    def _validate(self):
        required = {'date', 'value'}
        if not required.issubset(self.df.columns):
            raise ValueError(f'{self.name} missing required columns')

        self.df['date'] = pd.to_datetime(self.df['date'])
        self.df = self.df.sort_values('date')

    def to_frame(self):
        df = self.df.copy()
        df['signal'] = self.name
        return df

    def resample(self, freq='D', method='mean'):
        df = self.df.set_index('date')

        if method == 'mean':
            df = df.resample(freq).mean()
        elif method == 'sum':
            df = df.resample(freq).sum()

        df = df.reset_index()
        return Signal(self.name, df)

    def add_lag(self, periods=1):
        df = self.df.copy()
        df['value'] = df['value'].shift(periods)
        return Signal(f'{self.name}_lag_{periods}', df)
    