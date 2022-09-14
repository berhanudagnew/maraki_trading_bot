# from binance.spot import Spot
import pandas as pd
import ccxt
import talib
import pandas_ta as ta
import time
import asyncio
# from convert import DateConverter

api_client = ccxt.binance()
# conv_date = DateConverter()
class GetLiveData:  
    
    def __init__(self, _symbol, _time_interval, _limit):
        self.symbol = _symbol
        self.time_interval = _time_interval
        self.limit = _limit
        self.df = []
        self.talib = talib
        
    async def data_1_minute(self):
        print("Running get_1_minute API data")
        await asyncio.sleep(0)
        my_time_interval = '1m'
        # Get last 10 klines of BNBUSDT at 1h interval
        candle_data = api_client.fetch_ohlcv(self.symbol, my_time_interval, limit = self.limit)
        self.df = pd.DataFrame(candle_data, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
        self.df['time'] = pd.to_datetime(self.df['time'], unit='ms')
        self.df = pd.concat([self.df, self.df.ta.rsi()], axis=1)
        self.df.to_csv(f'original_data_{my_time_interval}_minute.csv')
    
        print("Finished get_1_minute API dat")
        return self.df
    async def data_3_minute(self):
        print("Running get_3_minute API data")
        await asyncio.sleep(0)
        my_time_interval = "3m"
        # Get last 10 klines of BNBUSDT at 1h interval
        candle_data = api_client.fetch_ohlcv(self.symbol, my_time_interval, limit = self.limit)
        self.df = pd.DataFrame(candle_data, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
        self.df['time'] = pd.to_datetime(self.df['time'], unit='ms')
        self.df = pd.concat([self.df, self.df.ta.rsi()], axis=1)
        self.df.to_csv(f'original_data_{my_time_interval}_minute.csv')
       
        print("Finished get_3_minute API dat")
        return self.df 

    async def market_data(self):
          
        task_1 = asyncio.create_task(self.data_1_minute())
        task_2 = asyncio.create_task(self.data_3_minute())
        # value_1 = await task_1
        # value_2 = await task_2
        await task_1
        await task_2
