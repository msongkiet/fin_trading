import yfinance as yf

def get_yf_price(ticker, period = '3mo'):
    """ Get stock historical data from Yahoo Finance

    Args : 
        - ticker : Stock qoute in https://finance.yahoo.com/
        - period : valid period --> 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max (optional is '3mo')

    Return :
        - df : stock historical dataframe

    """
    try:
        df = yf.Ticker(ticker)
        df = df.history(period=period)
        df = df.drop(columns=['Dividends', 'Stock Splits'])
        df['ticker'] = ticker.split(".")[0]
        df['ohlc4'] = df[['Open', 'High', 'Low', 'Close']].mean(axis=1)
        df = df.drop(columns=['Open', 'High', 'Low', 'Close'])
        # print(df)
        return df
    except Exception as e:
        print(e)
