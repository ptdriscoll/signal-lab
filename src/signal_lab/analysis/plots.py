import matplotlib.pyplot as plt
import numpy as np


def plot_rolling_corr(df, col='rolling_corr', title='Rolling Correlation', save_path=None):
    plt.figure()

    df[col].plot()

    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Correlation')

    plt.axhline(0, linewidth=1)

    if save_path:
        plt.savefig(save_path, bbox_inches='tight')

    plt.show()
    plt.close()

def plot_event_study(
    df,
    signal_col='weather',
    target_col='market',
    window=5,
    title='Event Study',
    save_path=None
):
    df = df.reset_index(drop=True)

    results = []

    threshold = df[signal_col].std()
    events = df[df[signal_col] > threshold].index.tolist()

    for e in events:
        if e - window < 0 or e + window >= len(df):
            continue

        slice_ = df.iloc[e-window:e+window+1][target_col].values
        results.append(slice_)

    if not results:
        print('No events found')
        return

    avg = np.mean(results, axis=0)

    plt.figure()
    plt.plot(range(-window, window+1), avg)

    plt.title(title)
    plt.xlabel('Days Around Event')
    plt.ylabel(f'Average {target_col} Move')

    plt.axhline(0, linewidth=1)

    if save_path:
        plt.savefig(save_path, bbox_inches='tight')

    plt.show()
    plt.close()    
