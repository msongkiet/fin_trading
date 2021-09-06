from yf_price import get_yf_price
from cdc_indi import cdc_indi
from cdc_scan import cdc_scan
from line_notify import line_notify

import pandas as pd
import os

token = os.environ.get('token_line_trading_signal')
googleSheetId = os.environ.get('googleSheetId_quote')

worksheetName = ['SET100', 'sSET']

for i in range(len(worksheetName)):
    url_google_sheet = 'https://docs.google.com/spreadsheets/d/{0}/gviz/tq?tqx=out:csv&sheet={1}'.format(googleSheetId, worksheetName[i])
    tickers = pd.read_csv(url_google_sheet)
    tickers = (tickers['Quote'].values.tolist())

    msg_golden_cross = ''
    msg_dead_cross = ''
    msg_pre_buy = ''
    msg_pre_sell = ''

    for j in range(len(tickers)):
        try:
            price_df = get_yf_price(tickers[j])
            price_df = cdc_indi(price_df)
            signal = cdc_scan(price_df)
            if(len(signal)!=0):
                if(signal == 'bullish'):
                    msg_golden_cross += f'{tickers[j].split(".")[0]} '
                elif(signal == 'bearish'):
                    msg_dead_cross += f'{tickers[j].split(".")[0]} '
                elif(signal == 'blue'):
                    msg_pre_buy += f'{tickers[j].split(".")[0]} '
                elif(signal == 'yellow'):
                    msg_pre_sell += f'{tickers[j].split(".")[0]} '
        except Exception as e:
            print(e)

    line_notify(f'{worksheetName[i]} CDC Golden Cross: {msg_golden_cross}', token)
    line_notify(f'{worksheetName[i]} CDC Dead Cross: {msg_dead_cross}', token)
    line_notify(f'{worksheetName[i]} CDC Pre-Buy Zone: {msg_pre_buy}', token)
    line_notify(f'{worksheetName[i]} CDC Pre-Sell Zone: {msg_pre_sell}', token)