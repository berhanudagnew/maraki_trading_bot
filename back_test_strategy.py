from turtle import pd
from get_data import GetData
from order import Order
import talib
import pandas as pd
from functions.my_colors import colors as c
import talib

class BackTestStrategy():
    
    def ema_method_1m(self):
        df = pd.read_csv('update_data_1m_minute.csv')
        total_share_long_quantity = 1
        # for 4% profit
        profit_limit = 0.02
        # for 2% risk
        risck_limit = 0.02
        # stop for best profit 
        best_profit = 0
        # market start and end time YY-MM-DD-HH-mm
        start_date = 2020, 1, 3, 1, 0
        end_date = 2020, 12, 29, 21, 0

        period = 14
        indicator_type = 'RSI_14'
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

        for i in range(len(df['close'])):
            # buy long trade methode
            #    if  (buy_long_order == True) & (sell_long_order == False) & (str(df['date'][i]) != previouse_order_date) & (previous_long_buy_price < df['c'][i]):
            #         # get_web.close_market_order_long(stock_quantity)
            #         # Updater
            #         previous_long_buy_price = df['c'][i]
            # integer = CDL3INSIDE(open, high, low, close)
            if (df['RSI_14'][i] < 50) & (df['ema_4'][i] < df['ema_15'][i]) & (df['macd'][i] < df['macdSignal'][i])& (sell_long_order == True) & (buy_long_order == False)\
                    & (str(df['time'][i]) != previouse_order_date):
                    # get_web.symboll_adder(stock_symbol)
                    # get_web.buy_market_long(stock_quantity)
                    buy_long_order = True
                    sell_long_order = False
                    previous_long_buy_price = df['close'][i]
                    original_long_buy_price = df['close'][i]
                    print(i, c.fg.green + 'Buy Long' + c.reset, df['time'][i], df['close'][i], previous_long_buy_price)
                    previouse_order_date = str(df['time'][i])
                    pdt_counter = pdt_counter + 1
                    print(c.fg.pink + 'PDT counter '+c.reset, pdt_counter)
                # Sell in Long trade method

            if (df['RSI_14'][i] > 55) & (df['ema_4'][i] > df['ema_15'][i]) & (df['macd'][i] > df['macdSignal'][i]) & (buy_long_order == True) & (sell_long_order == False) \
                    & (df['close'][i] >= (original_long_buy_price+(original_long_buy_price * profit_limit))) & (str(df['time'][i]) != previouse_order_date):
                    # get_web.close_market_order_long(stock_quantity)
                    buy_long_order = False
                    sell_long_order = True
                    
                    print(i, c.fg.blue + 'Sell Long' + c.reset, df['time'][i], df['close'][i], previous_long_buy_price)
                    # calculate sum
                    buy_long_temp_price = original_long_buy_price
                    sell_long_temp_price = df['close'][i]
                    # total_share_long_price = int(total_share_long_quantity) * buy_long_temp_price
                    print((sell_long_temp_price-buy_long_temp_price),(sell_long_temp_price-buy_long_temp_price) * total_share_long_quantity)
                    total_long_profit = total_long_profit + ((sell_long_temp_price - buy_long_temp_price) * total_share_long_quantity)
                    print(c.fg.orange + "Long total profit " +c.reset ,total_long_profit)
                
                    previouse_order_date = str(df['time'][i])

                    # Protect excess risk
                    # STTOP LOSS 
            if (df['close'][i] <= (previous_long_buy_price - (previous_long_buy_price * risck_limit))) & (buy_long_order == True)\
                    & (sell_long_order == False) & (str(df['time'][i]) != previouse_order_date):
                    # get_web.close_market_order_long(stock_quantity)
                    print("STOP LOSS")
                    buy_long_order = False
                    sell_long_order = True

                    print(i, c.fg.red + 'Sell Long Risk' +c.reset, df['time'][i], df['close'][i], previous_long_buy_price)
                    # calculate sum
                    buy_long_temp_price = original_long_buy_price
                    sell_long_temp_price = df['close'][i]
                    # total_share_long_price = int(total_share_long_quantity) * buy_long_temp_price
                    print((sell_long_temp_price-buy_long_temp_price),(sell_long_temp_price - buy_long_temp_price) * total_share_long_quantity)
                    total_long_profit = total_long_profit + ((sell_long_temp_price - buy_long_temp_price) * total_share_long_quantity)
                    print(c.fg.red + "Long total profit " + c.reset, total_long_profit)

                    previouse_order_date = str(df['time'][i])
    
        # integer = CDL3INSIDE(open, high, low, close)   
    def candle_method_1m(self):
        df = pd.read_csv('update_data_1m_minute.csv')
        total_share_long_quantity = 1
        # for 4% profit
        profit_limit = 0.02
        # for 2% risk
        risck_limit = 0.02
        # stop for best profit 
        best_profit = 0
        # market start and end time YY-MM-DD-HH-mm
        start_date = 2020, 1, 3, 1, 0
        end_date = 2020, 12, 29, 21, 0

        period = 14
        indicator_type = 'RSI_14'
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

        for i in range(len(df['close'])):
            # buy long trade methode
            #    if  (buy_long_order == True) & (sell_long_order == False) & (str(df['date'][i]) != previouse_order_date) & (previous_long_buy_price < df['c'][i]):
            #         # get_web.close_market_order_long(stock_quantity)
            #         # Updater
            #         previous_long_buy_price = df['c'][i]

            if (df['RSI_14'][i] < 50) & (df['ema_4'][i] < df['ema_15'][i]) & (df['macd'][i] < df['macdSignal'][i])& (sell_long_order == True) & (buy_long_order == False)\
                    & (str(df['time'][i]) != previouse_order_date):
                    # get_web.symboll_adder(stock_symbol)
                    # get_web.buy_market_long(stock_quantity)
                    buy_long_order = True
                    sell_long_order = False
                    previous_long_buy_price = df['close'][i]
                    original_long_buy_price = df['close'][i]
                    print(i, c.fg.green + 'Buy Long' + c.reset, df['time'][i], df['close'][i], previous_long_buy_price)
                    previouse_order_date = str(df['time'][i])
                    pdt_counter = pdt_counter + 1
                    print(c.fg.pink + 'PDT counter '+c.reset, pdt_counter)
                # Sell in Long trade method

            if (df['RSI_14'][i] > 55) & (df['ema_4'][i] > df['ema_15'][i]) & (df['macd'][i] > df['macdSignal'][i]) & (buy_long_order == True) & (sell_long_order == False) \
                    & (df['close'][i] >= (original_long_buy_price+(original_long_buy_price * profit_limit))) & (str(df['time'][i]) != previouse_order_date):
                    # get_web.close_market_order_long(stock_quantity)
                    buy_long_order = False
                    sell_long_order = True
                    
                    print(i, c.fg.blue + 'Sell Long' + c.reset, df['time'][i], df['close'][i], previous_long_buy_price)
                    # calculate sum
                    buy_long_temp_price = original_long_buy_price
                    sell_long_temp_price = df['close'][i]
                    # total_share_long_price = int(total_share_long_quantity) * buy_long_temp_price
                    print((sell_long_temp_price-buy_long_temp_price),(sell_long_temp_price-buy_long_temp_price) * total_share_long_quantity)
                    total_long_profit = total_long_profit + ((sell_long_temp_price - buy_long_temp_price) * total_share_long_quantity)
                    print(c.fg.orange + "Long total profit " +c.reset ,total_long_profit)
                
                    previouse_order_date = str(df['time'][i])

                    # Protect excess risk
                    # STTOP LOSS 
            if (df['close'][i] <= (previous_long_buy_price - (previous_long_buy_price * risck_limit))) & (buy_long_order == True)\
                    & (sell_long_order == False) & (str(df['time'][i]) != previouse_order_date):
                    # get_web.close_market_order_long(stock_quantity)
                    print("STOP LOSS")
                    buy_long_order = False
                    sell_long_order = True
                    # TODO@berhanudagnew
                    print(i, c.fg.red + 'Sell Long Risk' +c.reset, df['time'][i], df['close'][i], previous_long_buy_price)
                    # calculate sum
                    buy_long_temp_price = original_long_buy_price
                    sell_long_temp_price = df['close'][i]
                    # total_share_long_price = int(total_share_long_quantity) * buy_long_temp_price
                    print((sell_long_temp_price-buy_long_temp_price),(sell_long_temp_price - buy_long_temp_price) * total_share_long_quantity)
                    total_long_profit = total_long_profit + ((sell_long_temp_price - buy_long_temp_price) * total_share_long_quantity)
                    print(c.fg.red + "Long total profit " + c.reset, total_long_profit)

                    previouse_order_date = str(df['time'][i])