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
class UpdateLiveData:
        
    async def update_1_minute(self):
        print("Running update_1m data")
        await asyncio.sleep(0)
        my_time_interval = "1m"
        df = pd.read_csv("original_data_1m_minute.csv")
        df['ema_4']= talib.EMA(df['close'],4)
        df['ema_15']= talib.EMA(df['close'],15)
        df['macd'], df['macdSignal'], df['macdHist'] = talib.MACD(df['close'], fastperiod=2, slowperiod=14, signalperiod=12)
        df.to_csv(f'update_data_{my_time_interval}_minute.csv')
        
        print("Finished update_1m data")
        return df
    async def update_3_minute(self):
        print("Running update_3m data")
        await asyncio.sleep(0)
        my_time_interval = "3m"
        df = pd.read_csv("original_data_3m_minute.csv")
        df['ema_4']= talib.EMA(df['close'],4)
        df['ema_15']= talib.EMA(df['close'],15)
        df['macd'], df['macdSignal'], df['macdHist'] = talib.MACD(df['close'], fastperiod=2, slowperiod=14, signalperiod=12)
        df.to_csv(f'update_data_{my_time_interval}_minute.csv')
      
        print("Finished update_3m data")
        return df 

    async def update_data(self):
          
        task_1 = asyncio.create_task(self.update_1_minute())
        task_2 = asyncio.create_task(self.update_3_minute())
        # value_1 = await task_1
        # value_2 = await task_2
        await task_1
        await task_2
