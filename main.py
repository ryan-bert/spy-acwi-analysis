import pandas as pd
from plotnine import ggplot, aes, geom_line, labs

def main():

    # Load returns data
    returns_df = pd.read_csv('~/Documents/Financial Data/daily_etf_index_returns.csv')
    returns_df['Date'] = pd.to_datetime(returns_df['Date'])

    # Select only SPY and ACWI
    returns_df = returns_df[['Date', 'SPY', 'ACWI']]

    # Remove initial 0 returns
    start_date = returns_df[(returns_df['SPY'] != 0) & (returns_df['ACWI'] != 0)]['Date'].min()
    returns_df = returns_df[returns_df['Date'] >= start_date].reset_index(drop=True)

    # Calculate cumulative returns
    returns_df['SPY_cumulative'] = (1 + returns_df['SPY']).cumprod()
    returns_df['ACWI_cumulative'] = (1 + returns_df['ACWI']).cumprod()
    
    # Plot cumulative returns
    plot = (
        ggplot() +
        geom_line(returns_df, aes(x='Date', y='SPY_cumulative'), color='blue') +
        geom_line(returns_df, aes(x='Date', y='ACWI_cumulative'), color='red') +
        labs(title='Cumulative Returns of SPY and ACWI',
             x='Date',
             y='Cumulative Return')
    )
    print(plot)


if __name__ == '__main__':
    main()