import os
import pandas as pd
from plotnine import ggplot, aes, geom_line, labs, theme_minimal

CRISES_PERIODS = {
    "Global Financial Crisis": {"start": "2007-08-01", "end": "2009-06-30"},
    "European Sovereign Debt Crisis": {"start": "2010-01-01", "end": "2012-12-31"},
    "Chinese Stock Market Turmoil": {"start": "2015-06-01", "end": "2016-02-29"},
    "COVID-19 Crash": {"start": "2020-02-01", "end": "2020-11-30"},
    "Crypto Winter and Tech Stock Correction": {"start": "2021-11-01", "end": "2022-12-31"},
    "Energy and Inflation Crisis": {"start": "2022-03-01", "end": "2023-06-30"},
}

def main():
    # Ensure the plots directory exists
    output_dir = '/Users/ryanbertschinger/Documents/GitHub/spy-acwi-analysis/plots/'
    os.makedirs(output_dir, exist_ok=True)

    # Load returns data
    returns_df = pd.read_csv('~/Documents/Financial Data/daily_etf_index_returns.csv')
    returns_df['Date'] = pd.to_datetime(returns_df['Date'])
    returns_df = returns_df[['Date', 'SPY', 'ACWI']]

    # Remove initial 0 returns
    start_date = returns_df[(returns_df['SPY'] != 0) & (returns_df['ACWI'] != 0)]['Date'].min()
    returns_df = returns_df[returns_df['Date'] >= start_date].reset_index(drop=True)

    # Convert crisis periods to datetime
    for crisis, dates in CRISES_PERIODS.items():
        dates['start'] = pd.to_datetime(dates['start'])
        dates['end'] = pd.to_datetime(dates['end'])

    # Calculate cumulative returns for the full dataset
    returns_df['SPY cumulative'] = (1 + returns_df['SPY']).cumprod()
    returns_df['ACWI cumulative'] = (1 + returns_df['ACWI']).cumprod()

    # Function to analyze and plot each crisis
    def analyze_crisis(crisis_name):
        crisis_df = returns_df[
            (returns_df['Date'] >= CRISES_PERIODS[crisis_name]['start']) &
            (returns_df['Date'] <= CRISES_PERIODS[crisis_name]['end'])
        ].copy()

        # Calculate cumulative returns
        crisis_df['SPY cumulative'] = (1 + crisis_df['SPY']).cumprod()
        crisis_df['ACWI cumulative'] = (1 + crisis_df['ACWI']).cumprod()

        # Melt the DataFrame for plotting
        crisis_melted = crisis_df.melt(
            id_vars=['Date'],
            value_vars=['SPY cumulative', 'ACWI cumulative'],
            var_name='Asset',
            value_name='Cumulative Return'
        )

        # Create the plot
        crisis_plot = (
            ggplot(crisis_melted, aes(x='Date', y='Cumulative Return', color='Asset')) +
            geom_line() +
            labs(title=f'Cumulative Returns during {crisis_name}',
                 x='Date',
                 y='Cumulative Return')
        )

        # Save the plot
        crisis_plot.save(f'{output_dir}/{crisis_name.replace(" ", "_").lower()}_plot.png')

    # Analyze each crisis
    for crisis_name in CRISES_PERIODS.keys():
        analyze_crisis(crisis_name)

    # Plot cumulative returns for the entire dataset
    returns_melted = returns_df.melt(
        id_vars=['Date'],
        value_vars=['SPY cumulative', 'ACWI cumulative'],
        var_name='Asset',
        value_name='Cumulative Return'
    )
    full_plot = (
        ggplot(returns_melted, aes(x='Date', y='Cumulative Return', color='Asset')) +
        geom_line() +
        labs(title='Cumulative Returns of SPY and ACWI',
             x='Date',
             y='Cumulative Return')
    )
    full_plot.save(f'{output_dir}/returns_plot.png')

if __name__ == '__main__':
    main()