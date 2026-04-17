from signal_lab.domain.signals import Signal

def run(data_dict):
    signals = []

    for name, df in data_dict.items():
        signal = Signal(name, df)
        signals.append(signal)

    return signals
