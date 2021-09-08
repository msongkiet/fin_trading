from yf_price import get_yf_price
from cdc_indi import cdc_indi
from cdc_scan import cdc_scan
from vol_indi import vol_indi
from line_notify import line_notify

import pandas as pd
import os

# token = os.environ.get('token_line_trading_signal')
token = os.environ.get('token_line_test')
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
    df_vol = pd.DataFrame()

    for j in range(len(tickers)):
        try:
            df_price = get_yf_price(tickers[j])
            df_price = cdc_indi(df_price)
            df_price = vol_indi(df_price)
            df_vol = df_vol.append(df_price.tail(1),ignore_index=False)

            signal = cdc_scan(df_price)
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

    df_vol = df_vol.sort_values(by=['x_of_vol_ma'],ascending=False)   
    msg_vol_change = ''

    for row in df_vol.itertuples():
        if row.x_of_vol_ma >= 1.50:
            msg_vol_change += f'{row.ticker}:{row.x_of_vol_ma}X, '
        else:
            break

    line_notify(f'{worksheetName[i]} CDC Golden Cross: {msg_golden_cross}', token)
    line_notify(f'{worksheetName[i]} CDC Dead Cross: {msg_dead_cross}', token)
    line_notify(f'{worksheetName[i]} CDC Pre-Buy Zone: {msg_pre_buy}', token)
    line_notify(f'{worksheetName[i]} CDC Pre-Sell Zone: {msg_pre_sell}', token)
    line_notify(f'{worksheetName[i]} Vol change (x of vol ma): {msg_vol_change}', token)
