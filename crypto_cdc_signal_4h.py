from binance_price import get_crypto_price
from cdc_indi import cdc_indi
from cdc_scan import cdc_scan
from line_notify import line_notify

import pandas as pd
import os

token = os.environ.get('token_line_trading_signal')
token1 = os.environ.get('token_line_defi_farmer')
googleSheetId = os.environ.get('googleSheetId_quote')

worksheetName = 'Crypto'
url_google_sheet = 'https://docs.google.com/spreadsheets/d/{0}/gviz/tq?tqx=out:csv&sheet={1}'.format(googleSheetId, worksheetName)
tickers = pd.read_csv(url_google_sheet)
tickers = (tickers['Quote'].values.tolist())

msg_golden_cross = ''
msg_dead_cross = ''
msg_pre_buy = ''
msg_pre_sell = ''
tf = '4h'

for j in range(len(tickers)):
    try:
        price_df = get_crypto_price(tickers[j], tf)
        price_df = cdc_indi(price_df)
        signal = cdc_scan(price_df)
        if(len(signal)!=0):
            if(signal == 'bullish'):
                msg_golden_cross += f'{tickers[j]} '
            elif(signal == 'bearish'):
                msg_dead_cross += f'{tickers[j]} '
            elif(signal == 'blue'):
                msg_pre_buy += f'{tickers[j]} '
            elif(signal == 'yellow'):
                msg_pre_sell += f'{tickers[j]} '
    except Exception as e:
        print(e)
        
line_notify(f'TF {tf} Crypto Golden Cross: {msg_golden_cross}', token)
line_notify(f'TF {tf} Crypto Dead Cross: {msg_dead_cross}', token)
line_notify(f'TF {tf} Crypto Pre-Buy Zone: {msg_pre_buy}', token)
line_notify(f'TF {tf} Crypto Pre-Sell Zone: {msg_pre_sell}', token)

line_notify(f'TF {tf} Crypto Golden Cross: {msg_golden_cross}', token1)
line_notify(f'TF {tf} Crypto Dead Cross: {msg_dead_cross}', token1)
line_notify(f'TF {tf} Crypto Pre-Buy Zone: {msg_pre_buy}', token1)
line_notify(f'TF {tf} Crypto Pre-Sell Zone: {msg_pre_sell}', token1)