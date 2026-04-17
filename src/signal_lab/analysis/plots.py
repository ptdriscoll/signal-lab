import matplotlib.pyplot as plt

def plot_rolling_corr(df):
    plt.figure()

    df['rolling_corr'].plot()

    plt.title('Rolling Correlation: Weather vs SP500')
    plt.xlabel('Date')
    plt.ylabel('Correlation')

    plt.axhline(0, linewidth=1)

    plt.show()
    
def plot_event_study(df):
    import matplotlib.pyplot as plt

    df = df.reset_index(drop=True)  # IMPORTANT FIX

    window = 5
    results = []

    events = df[df['weather'] > df['weather'].std()].index.tolist()

    for e in events:
        if e - window < 0 or e + window >= len(df):
            continue

        slice_ = df.iloc[e-window:e+window+1]['sp500'].values
        results.append(slice_)

    if not results:
        print('No events found')
        return

    avg = sum(results) / len(results)

    plt.figure()
    plt.plot(range(-window, window+1), avg)

    plt.title('Market Response Around Weather Extremes')
    plt.xlabel('Days Around Event')
    plt.ylabel('Average SP500 Move')
    plt.axhline(0, linewidth=1)
    plt.show()   
