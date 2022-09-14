import asyncio
from get_live_data import GetLiveData
from update_live_data import UpdateLiveData
from order import Order
# from plot_chart import PlotChart
# order_1  = Order()

# symbol, interval, limit = order_1.my_order()
# update_api_data = GetLiveData(symbol, interval, limit)
# asyncio.run(update_api_data.market_data())

import threading
import time
import schedule
from back_test_strategy import BackTestStrategy

def get_live_data():

    order_1  = Order()
    symbol, interval, limit = order_1.my_order()
    get_api_data = GetLiveData(symbol, interval, limit)

    asyncio.run(get_api_data.market_data())

def update_live_data():
    # create object for UpdateLiveData
    update_api_data = UpdateLiveData()
    # run asyncio main function to update both value
    asyncio.run(update_api_data.update_data())

def ema_stratagy():
    print('ema running ... ')
    strategy = BackTestStrategy()
    ema_method = strategy.ema_method_1m()
    print('ema finished !')
    return

def candle_stratagy():
    print('candle running ...')
    # live_method = LiveMethodOne()
    # live_method.live_method()
    print('candle finished !')

def start_bot():
    print('Bot running ... ')
    # inside Synci functions get and update data with out thrade
    # first get api data
    print('Start Get API data')
    get_live_data()
    print('finish get API data')
    # update API data ema macd ....
    print('Start update API data')
    update_live_data()
    print('finish update API data')

    # use thrade function to do multiple thecniques in same time

    
    # creating threade
    t1 = threading.Thread(target=ema_stratagy)
    t2 = threading.Thread(target=candle_stratagy)
    # start trade 1
    t1.start()
    t2.start()

    # wait untill threade 1 is completly excuted
    t1.join()
    t2.join()
    # Dra charts
    # draw_chart = PlotChart(ohlc_price.get_data())
    # draw_chart.view()
    print('BOT Succesfull !')
    return

start_bot()