from plotnine import ggplot, aes, geom_line, labs, theme_minimal
import pandas as pd

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
    returns_df['SPY cumulative'] = (1 + returns_df['SPY']).cumprod()
    returns_df['ACWI cumulative'] = (1 + returns_df['ACWI']).cumprod()

    # Melt the DataFrame for plotting
    returns_melted = returns_df.melt(
        id_vars=['Date'],
        value_vars=['SPY cumulative', 'ACWI cumulative'],
        var_name='Asset',
        value_name='Cumulative Return'
    )

    # Plot using color aesthetic for labels
    plot = (
        ggplot(returns_melted, aes(x='Date', y='Cumulative Return', color='Asset')) +
        geom_line() +
        labs(title='Cumulative Returns of SPY and ACWI',
             x='Date',
             y='Cumulative Return')
    )
    print(plot)

if __name__ == '__main__':
    main()