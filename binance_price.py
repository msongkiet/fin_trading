import requests
import json
import pandas as pd
import datetime as dt

def get_crypto_price(symbol, interval = '1d'):
    try:
        url = f'https://api.binance.com/api/v1/klines?symbol={symbol}&interval={interval}'
        data = json.loads(requests.get(url).text)
        df = pd.DataFrame(data)
        df.columns = ['open_time',
                     'o', 'h', 'l', 'c', 'v',
                     'close_time', 'qav', 'num_trades',
                     'taker_base_vol', 'taker_quote_vol', 'ignore']
        df.index = [dt.datetime.fromtimestamp(x/1000.0) for x in df.close_time]
        df.drop(columns=['open_time', 'v', 'close_time', 'qav', 'num_trades', 'taker_base_vol', 
                         'taker_quote_vol', 'ignore'], inplace = True)
        df = df.apply(pd.to_numeric, errors='coerce')
        df['ohlc4'] = df.mean(axis=1)
        df = df.drop(columns=['o','h','l','c'])

        return df

    except Exception as e:
        print(e)