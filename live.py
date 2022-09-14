import datetime
import pytz
import requests
import schedule
import time

import numpy as np
import pandas as pd

import talib

from json.decoder import JSONDecodeError

# custom library

import pyttsx3


# Variables
fin_api = 'cbrartaad3i32qd60l1g'
# AAPL, SYN, ADXS, CTRM, FAMI, AAU, NAKD, SONM, XPL, NVIV, AUMN, PLIN, INUV, GPL, USWS, SNDL, NXTD, AZRX, MKD, ISR, RMTI, UAMY, PULM, MYSZ, WEI, WTER, LMFA, SEAC 
stock_symbol = 'AR'
stock_quantity = '20'
price_limit = 0.02
# start_t = 1617264000 
# end_t =	1619848800
start_t = 1620318374# 3/03/21  1614762863   # 
end_t =	1620877405
# 1619593200 (28.0.0/04/2021) 1619420400 (26.0.0/04/2021)
period = 14
indicator_type = 'rsi'
time_interval = 15
previouse_order_date = 'a'
buy_order_long = False
sell_order_long = True

sell_order_short = False
buy_order_short = True

previous_long_buy_price = 1
previous_short_sell_price = 1

long_buy = 1
long_sell = 1
long_sum = 0

short_buy = 1
short_sell = 1
short_sum = 0
# text to audio
engine = pyttsx3.init()


url = f'https://finnhub.io/api/v1/indicator?symbol={stock_symbol}&resolution={time_interval}&from={start_t}&to={end_t}&indicator={indicator_type}&timeperiod={period}&token={fin_api}'

# functions
# time changer
def tim_changer(ts):
    d1 = datetime.datetime.fromtimestamp(int(ts))
    return d1.strftime("%d.%m.%y %H:%M:%S")
# text to audio
def play(text):
    engine.say(text)
    engine.runAndWait()

def get_server_data():
    try:
        res = requests.get(url)
        rsin = res.json()
        return rsin
    
    except ValueError as v:
        print(v)
        return 'no_value'
    except JSONDecodeError as e:
        print(e)
        return 'json_error'
    except TypeError as t:
        print(t)
        return 'type_error'
    except:
        return 'no_connection'

def update_stock():
    global previouse_order_date, buy_order_long, sell_order_long, buy_order_short, sell_order_short, previous_long_buy_price,\
    previous_short_sell_price, long_buy, long_sell, long_sum, short_buy, short_sell, short_sum
    finn_hub_result = get_server_data()
    if (finn_hub_result) == 'no_connection':
        print('No Internet conection')
        return
    if (finn_hub_result) == 'type_error':
        print('type error')
        return
    if (finn_hub_result) == 'json_error':
        print('json error')
        return
    if (finn_hub_result) == 'no_value':
        print('no value')
        return  
    
    if type(finn_hub_result) != dict:
        print('Not proper Pandas file')
        return
    if (finn_hub_result['s']) == 'no_data':
        print('No data on server')
        return
    df = pd.DataFrame(finn_hub_result)
    
    df['date']=df['t'].apply(lambda x: x if x==103 else tim_changer(x))
    df.index = df['date']

    df['ema_4']= talib.EMA(df['c'],4)
    df['ema_15']= talib.EMA(df['c'],15)
    df['macd'], df['macdSignal'], df['macdHist'] = talib.MACD(df['c'], fastperiod=2, slowperiod=10, signalperiod=14)

   
    i=0
    i = len(df['c'])-1
    print(df['date'][i], df['c'][i])
    # Buy in long trade method

    if (df['rsi'][i] < 45) & (df['ema_4'][i] < df['ema_15'][i]) & (df['macd'][i] < df['macdSignal'][i]) \
        & (buy_order_long == False) & (str(df['date'][i]) != previouse_order_date):
        # get_web.symboll_adder(stock_symbol)
        # get_web.buy_market_long(stock_quantity)
        buy_order_long = True
        sell_order_long = False
        previous_long_buy_price = df['c'][i]
        play('Buy Long ' + stock_symbol + ' ' + stock_quantity)
        print(i, 'Buy Long', df['date'][i], df['c'][i],previous_long_buy_price)
        previouse_order_date = str(df['date'][i])
    
    # Sell in Long trade method

    if (df['rsi'][i] > 53) & (df['ema_4'][i] > df['ema_15'][i]) & (df['macd'][i] > df['macdSignal'][i]) \
        & (df['c'][i] > (previous_long_buy_price+price_limit)) & (sell_order_long == False) & (str(df['date'][i]) != previouse_order_date):
        # get_web.close_market_order_long(stock_quantity)
        sell_order_long = True
        buy_order_long = False
        play('Sell Long ' + stock_symbol + ' ' + stock_quantity)
        print(i, 'Sell Long', df['date'][i], df['c'][i],previous_long_buy_price)
        # calculate sum
        long_buy = previous_long_buy_price
        long_sell = df['c'][i]
        stock_price_long = int(stock_quantity) * long_buy
        print((long_sell-long_buy),(long_sell-long_buy)*((stock_price_long+long_sum)/long_buy))
        long_sum = long_sum + ((long_sell-long_buy)*((stock_price_long+long_sum)/long_buy))
        print("Long total profit  ",long_sum)

        previouse_order_date = str(df['date'][i])
    
    # To check long trade profit
    # sum = 0
    # for b in range(len(sell)):
    #     print((sell[b]-buy[b]),(sell[b]-buy[b])*((500+sum)/buy[b]))
    #     sum = sum + ((sell[b]-buy[b])*((500+sum)/buy[b]))
    # print("total ",sum)   

    
    
    
    # Sell in Short trade method

    # if (df['rsi'][i] > 57) & (df['ema_4'][i] > df['ema_15'][i]) & (df['macd'][i] > df['macdSignal'][i]) \
    #     & (sell_order_short == False) & (str(df['date'][i]) != hold):
    #     get_web.symboll_adder(stock_symbol)
    #     get_web.sell_market_short(stock_quantity)
    #     sell_order_short = True
    #     buy_order_short = False
    #     previous_short_sell_price = df['c'][i]
    #     print(i, 'Sell Short', df['date'][i], df['c'][i],previous_short_sell_price)
    #     hold = str(df['date'][i])
    
    # # Buy in Short trade method

    # if (df['rsi'][i] < 52) & (df['ema_4'][i] < df['ema_15'][i]) & (df['macd'][i] < df['macdSignal'][i]) \
    #     & (df['c'][i] < (previous_short_sell_price-price_limit)) & (buy_order_short == False) & (str(df['date'][i]) != hold):
    #     get_web.close_market_order_short(stock_quantity)
    #     buy_order_short = True
    #     sell_order_short = False
    #     print(i, 'Buy Short', df['date'][i], df['c'][i],previous_short_sell_price)
    #     # calculate sum 
    #     short_sell = previous_short_sell_price
    #     short_buy = df['c'][i]
    #     stock_price_short = int(stock_quantity) * short_buy
    #     print((short_sell-short_buy),(short_sell-short_buy)*((stock_price_short+short_sum)/short_buy))
    #     short_sum = short_sum + ((short_sell-short_buy)*((stock_price_short+short_sum)/short_buy))
    #     print('Short total profit  ',short_sum) 
    #     hold = str(df['date'][i])
    
    i=0
    # To check short trade profit
    # sum = 0
    # for b in range(len(sell)):
    #     print((buy[b]-sell[b]),(buy[b]-sell[b])*((1000+sum)/sell[b]))
    #     sum = sum + ((buy[b]-sell[b])*((1000+sum)/sell[b]))
    # print("total ",sum)

def stock_job():
    print("update server")
    update_stock()
    return

# # Start
schedule.every(29).seconds.do(stock_job)

while True:
    schedule.run_pending()
    time.sleep(1) # wait one minute