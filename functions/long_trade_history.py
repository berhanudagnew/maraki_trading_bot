import talib
import pandas as pd
import sys
sys.path.append('.')
from functions.my_colors import colors as c
import datetime
import requests
fin_api = 'c246j52ad3i8ss341t20'
# Local time to Unix time Changer
def date_to_unix_changer(lts):
    unix_time = datetime.datetime(
    lts[0], lts[1], lts[2], lts[3], lts[4]).timestamp()
    return int(unix_time)
# functions
# UNIX time to local time changer
def unix_to_date_changer(ts):
    d1 = datetime.datetime.fromtimestamp(int(ts))
    return d1.strftime("%d.%m.%y %H:%M:%S")
def long_trade(stock_symbol, stock_quantity, time_interval, start_date, end_date, price_limit, risck_price):
    # Variables
    period = 14
    indicator_type = 'rsi'
    start_t = date_to_unix_changer(start_date)
    end_t = date_to_unix_changer(end_date)
    url = f'https://finnhub.io/api/v1/indicator?symbol={stock_symbol}&resolution={time_interval}&from={start_t}&to={end_t}&indicator={indicator_type}&timeperiod={period}&token={fin_api}'
    res = requests.get(url)
    rsin = res.json()
    hold = 'a'
    buy_order_long = False
    sell_order_long = True

    # sell_order_short = False
    # buy_order_short = True

    previous_long_buy_price = 1
    # previous_short_sell_price = 1

    long_buy = 1
    long_sell = 1
    long_sum = 0

    # short_buy = 1
    # short_sell = 1
    # short_sum = 0
    pdt_counter = 0
    df = pd.DataFrame(rsin)
    df['date'] = df['t'].apply(
        lambda x: x if x == 103 else unix_to_date_changer(x))
    df.index = df['date']

    df['ema_4'] = talib.EMA(df['c'], 4)
    df['ema_15'] = talib.EMA(df['c'], 15)
    df['macd'], df['macdSignal'], df['macdHist'] = talib.MACD(
        df['c'], fastperiod=2, slowperiod=10, signalperiod=14)
    for i in range(len(df['c'])):
        if (df['rsi'][i] < 45) & (df['ema_4'][i] < df['ema_15'][i]) & (df['macd'][i] < df['macdSignal'][i]) & (sell_order_long == True) \
                & (buy_order_long == False) & (str(df['date'][i]) != hold):
            # get_web.symboll_adder(stock_symbol)
            # get_web.buy_market_long(stock_quantity)
            buy_order_long = True
            sell_order_long = False
            previous_long_buy_price = df['c'][i]
            print(i, c.fg.green + 'Buy Long' + c.reset,
                  df['date'][i], df['c'][i], previous_long_buy_price)
            hold = str(df['date'][i])
            pdt_counter += 1
            print(c.fg.pink + 'PDT counter '+c.reset, pdt_counter)
        # Sell in Long trade method

        if (df['rsi'][i] > 53) & (df['ema_4'][i] > df['ema_15'][i]) & (df['macd'][i] > df['macdSignal'][i]) & (buy_order_long == True)\
                & (df['c'][i] >= (previous_long_buy_price+(previous_long_buy_price*price_limit))) & (sell_order_long == False) & (str(df['date'][i]) != hold):
            # get_web.close_market_order_long(stock_quantity)
            sell_order_long = True
            buy_order_long = False

            print(i, c.fg.blue + 'Sell Long' + c.reset,
                  df['date'][i], df['c'][i], previous_long_buy_price)
            # calculate sum
            long_buy = previous_long_buy_price
            long_sell = df['c'][i]
            stock_price_long = int(stock_quantity) * long_buy
            print((long_sell-long_buy), (long_sell-long_buy)
                  * ((stock_price_long+long_sum)/long_buy))
            long_sum = long_sum + ((long_sell-long_buy)
                                   * ((stock_price_long+long_sum)/long_buy))
            print(c.fg.orange + "Long total profit " + c.reset, long_sum)

            hold = str(df['date'][i])
        if (df['c'][i] <= (previous_long_buy_price - (previous_long_buy_price*risck_price))) & (buy_order_long == True)\
                & (sell_order_long == False) & (str(df['date'][i]) != hold):
            # get_web.close_market_order_long(stock_quantity)
            sell_order_long = True
            buy_order_long = False

            print(i, c.fg.red + 'Sell Long Risk' + c.reset,
                  df['date'][i], df['c'][i], previous_long_buy_price)
            # calculate sum
            long_buy = previous_long_buy_price
            long_sell = df['c'][i]
            stock_price_long = int(stock_quantity) * long_buy
            print((long_sell-long_buy), (long_sell-long_buy)
                  * ((stock_price_long+long_sum)/long_buy))
            long_sum = long_sum + ((long_sell-long_buy)
                                   * ((stock_price_long+long_sum)/long_buy))
            print(c.fg.red + "Long total profit  " + c.reset, long_sum)

            hold = str(df['date'][i])

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