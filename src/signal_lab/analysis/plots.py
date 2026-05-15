import matplotlib.pyplot as plt
import numpy as np


def plot_rolling_corr(df, col='rolling_corr', title='Rolling Correlation', save_path=None):
    """Generates a line chart of specified column, and includes baseline marker."""
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
    """
    Plots the average percentage change of a target metric surrounding an event.

    Events can be identified by a pre-computed binary signal_col or by exceeding 
    a standard deviation threshold:

    Notes
    -----
    This function automatically detects if signal_col format is binary or not: 
    1. Binary Mode: Column contains 0s and 1s, with '1' as an extreme event day.
    2. Raw Mode: Uses standard deviation and absolute values to flag extremes. 

    How this function processes your data:
    * Isolates Event Catalysts: Locates the exact row index for every 
      significant shock (Day 0).
    * Extracts Relative Windows: Slices uniform blocks of target data 
      surrounding each event (from 'window' days before to 'window' days after).
    * Discards Border Hazards: Skips events occurring too close to the start or end
      of the dataset to prevent incomplete tracking.
    * Aggregates Multi-Event History: Stacks all isolated windows and 
      calculates their mathematical average to find the typical behavior 
      across all historical shocks.
    * Visualizes the Impact: Generates a line graph centered on Day 0 with a 
      horizontal baseline at zero to highlight abnormal market movements.

    Internal Representation Matrix (window=2)
    -----------------------------------------
    If two extreme weather events occurred historically, the function aligns 
    them by 'Days Around Event' before calculating the plotted average:

    Relative Day | Event 1 Move (%) | Event 2 Move (%) | Plotted Average
    ------------ | ---------------- | ---------------- | ---------------
    Day -2       | -0.5             |  0.1             | -0.20
    Day -1       | -0.2             | -0.4             | -0.30
    Day  0       |  1.2             |  0.8             |  1.00 <-- (The Shock)
    Day +1       |  0.4             |  0.2             |  0.30
    Day +2       | -0.1             |  0.3             |  0.10
    """
    df = df.reset_index(drop=True)

    results = []

    #check for pre-computed binary signals
    is_binary = set(df[signal_col].dropna().unique()).issubset({0, 1, 0.0, 1.0})    
    if is_binary:
        events = df[df[signal_col] == 1].index.tolist()
    else:
        threshold = df[signal_col].std()
        events = df[df[signal_col].abs() > threshold].index.tolist()

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
