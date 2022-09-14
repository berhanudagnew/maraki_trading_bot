import datetime
import requests

from functions.my_colors import colors as c
from json.decoder import JSONDecodeError
import pandas as pd

import talib




# Variables
fin_api = 'cbrartaad3i32qd60l1g'
# AAPL, SYN, ADXS, CTRM, FAMI, AAU, NAKD, SONM, XPL, NVIV, AUMN, PLIN, INUV, GPL, USWS, SNDL, NXTD, AZRX, MKD, ISR, RMTI, UAMY, PULM, MYSZ, WEI, WTER, LMFA, SEAC 
stock_symbol = 'BINANCE:BTCUSDT'
total_share_long_quantity = 1
# for 4% profit
profit_limit = 0.02
# for 2% risk
risck_limit = 0.02
# stop for best profit 
best_profit = 0
# market start and end time YY-MM-DD-HH-mm
start_date = 2022, 8, 3, 1, 0
end_date = 2022, 8, 29, 21, 0

period = 14
indicator_type = 'rsi'
time_interval = 1
previouse_order_date = 'a'
buy_long_order = False
sell_long_order = True

sell_order_short = False
buy_order_short = True

previous_long_buy_price = 1
original_long_buy_price = 1
previous_short_sell_price = 1

buy_long_temp_price = 1
sell_long_temp_price = 1
total_long_profit = 0

short_buy = 1
short_sell = 1
short_sum = 0
pdt_counter = 0

# Local time to Unix time Changer
def date_to_unix_changer(lts):
    unix_time = datetime.datetime(lts[0], lts[1], lts[2], lts[3], lts[4]).timestamp()
    return int(unix_time)
start_t = date_to_unix_changer(start_date)
end_t = date_to_unix_changer(end_date)

url = f'https://finnhub.io/api/v1/indicator?symbol={stock_symbol}&resolution={time_interval}&from={start_t}&to={end_t}&indicator={indicator_type}&timeperiod={period}&token={fin_api}'


# functions
# Local time to Unix time Changer
def date_to_unix_changer(lts):
    unix_time = datetime.datetime(lts[0], lts[1], lts[2], lts[3], lts[4]).timestamp()
    return unix_time
# UNIX time to local time changer
def unix_to_date_changer(ts):
    d1 = datetime.datetime.fromtimestamp(int(ts))
    return d1.strftime("%d.%m.%y %H:%M:%S")

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
finn_hub_result = get_server_data()
if (finn_hub_result) == 'no_connection':
    print('No Internet conection')
    exit
if (finn_hub_result) == 'type_error':
    print('type error')
    exit
if (finn_hub_result) == 'json_error':
    print('json error')
    exit
if (finn_hub_result) == 'no_value':
    print('no value')
    exit  

if type(finn_hub_result) != dict:
    print('Not proper Pandas file')
    exit
if (finn_hub_result['s']) == 'no_data':
    print('No data on server')
    exit

df = pd.DataFrame(finn_hub_result)

df['date']=df['t'].apply(lambda x: x if x==103 else unix_to_date_changer(x))
df.index = df['date']


df['ema_4']= talib.EMA(df['c'],4)
df['ema_15']= talib.EMA(df['c'],15)
df['macd'], df['macdSignal'], df['macdHist'] = talib.MACD(df['c'], fastperiod=2, slowperiod=10, signalperiod=14)




for i in range(len(df['c'])):
   # buy long trade methode
#    if  (buy_long_order == True) & (sell_long_order == False) & (str(df['date'][i]) != previouse_order_date) & (previous_long_buy_price < df['c'][i]):
#         # get_web.close_market_order_long(stock_quantity)
#         # Updater
#         previous_long_buy_price = df['c'][i]
   if (df['rsi'][i] < 45) & (df['ema_4'][i] < df['ema_15'][i]) & (df['macd'][i] < df['macdSignal'][i])& (sell_long_order == True) & (buy_long_order == False)\
         & (str(df['date'][i]) != previouse_order_date):
        # get_web.symboll_adder(stock_symbol)
        # get_web.buy_market_long(stock_quantity)
        buy_long_order = True
        sell_long_order = False
        previous_long_buy_price = df['c'][i]
        original_long_buy_price = df['c'][i]
        print(i, c.fg.green + 'Buy Long' + c.reset, df['date'][i], df['c'][i], previous_long_buy_price)
        previouse_order_date = str(df['date'][i])
        pdt_counter = pdt_counter + 1
        print(c.fg.pink + 'PDT counter '+c.reset, pdt_counter)
    # Sell in Long trade method

   if (df['rsi'][i] > 53) & (df['ema_4'][i] > df['ema_15'][i]) & (df['macd'][i] > df['macdSignal'][i]) & (buy_long_order == True) & (sell_long_order == False) \
        & (df['c'][i] >= (original_long_buy_price+(original_long_buy_price * profit_limit))) & (str(df['date'][i]) != previouse_order_date):
        # get_web.close_market_order_long(stock_quantity)
        buy_long_order = False
        sell_long_order = True
        
        print(i, c.fg.blue + 'Sell Long' + c.reset, df['date'][i], df['c'][i], previous_long_buy_price)
        # calculate sum
        buy_long_temp_price = original_long_buy_price
        sell_long_temp_price = df['c'][i]
        # total_share_long_price = int(total_share_long_quantity) * buy_long_temp_price
        print((sell_long_temp_price-buy_long_temp_price),(sell_long_temp_price-buy_long_temp_price) * total_share_long_quantity)
        total_long_profit = total_long_profit + ((sell_long_temp_price - buy_long_temp_price) * total_share_long_quantity)
        print(c.fg.orange + "Long total profit " +c.reset ,total_long_profit)
    
        previouse_order_date = str(df['date'][i])

        # Protect excess risk
        # STTOP LOSS 
   if (df['c'][i] <= (previous_long_buy_price - (previous_long_buy_price * risck_limit))) & (buy_long_order == True)\
        & (sell_long_order == False) & (str(df['date'][i]) != previouse_order_date):
        # get_web.close_market_order_long(stock_quantity)
        print("STOP LOSS")
        buy_long_order = False
        sell_long_order = True

        print(i, c.fg.red + 'Sell Long Risk' +c.reset, df['date'][i], df['c'][i], previous_long_buy_price)
        # calculate sum
        buy_long_temp_price = original_long_buy_price
        sell_long_temp_price = df['c'][i]
        # total_share_long_price = int(total_share_long_quantity) * buy_long_temp_price
        print((sell_long_temp_price-buy_long_temp_price),(sell_long_temp_price - buy_long_temp_price) * total_share_long_quantity)
        total_long_profit = total_long_profit + ((sell_long_temp_price - buy_long_temp_price) * total_share_long_quantity)
        print(c.fg.red + "Long total profit " + c.reset, total_long_profit)

        previouse_order_date = str(df['date'][i])

#    if  (buy_order_long == True) & (sell_order_long == False) & (str(df['date'][i]) != hold):
#         # get_web.close_market_order_long(stock_quantity)
        
        
#         # Updater
#         # long_update_price = previous_long_buy_price
#         u_r = 2/100
#         if (df['c'][i] > (long_update_price+(previous_long_buy_price*u_r))):
#             long_update_price = df['c'][i]
#             # min_rsi = 35
#         if (df['c'][i] <= (long_update_price - (long_update_price*risck_price))):
#             sell_order_long = True
#             buy_order_long = False
#             print(i, c.fg.red + 'Sell Long Update' +c.reset, df['date'][i], df['c'][i],previous_long_buy_price,long_update_price)
#             # calculate sum
#             long_buy = previous_long_buy_price
#             long_sell = df['c'][i]
#             stock_price_long = int(stock_quantity) * long_buy
#             print((long_sell-long_buy),(long_sell-long_buy)*((stock_price_long+long_sum)/long_buy))
#             long_sum = long_sum + ((long_sell-long_buy)*((stock_price_long+long_sum)/long_buy))
#             print(c.fg.red + "Long total profit Updat  " +c.reset,long_sum)

#             hold = str(df['date'][i])  
#    if(buy_order_long == True):
#         long_buy = previous_long_buy_price
#         change = df['c'][i] - long_buy
#         print(i, c.fg.yellow + str(change*100/long_buy),' %'+c.reset)
#    if (df['c'][i] >= (previous_long_buy_price + (previous_long_buy_price*price_limit))) & (buy_order_long == True)\
#         & (sell_order_long == False) & (str(df['date'][i]) != hold):
#         # get_web.close_market_order_long(stock_quantity)
#         sell_order_long = True
#         buy_order_long = False

#         print(i, c.fg.red + 'Sell Long Risk' +c.reset, df['date'][i], df['c'][i],previous_long_buy_price)
#         # calculate sum
#         long_buy = previous_long_buy_price
#         long_sell = df['c'][i]
#         stock_price_long = int(stock_quantity) * long_buy
#         print((long_sell-long_buy),(long_sell-long_buy)*((stock_price_long+long_sum)/long_buy))
#         long_sum = long_sum + ((long_sell-long_buy)*((stock_price_long+long_sum)/long_buy))
#         print(c.fg.red + "Long total profit  " +c.reset,long_sum)

#         hold = str(df['date'][i])

