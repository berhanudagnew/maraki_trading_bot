# from binance.spot import Spot
import pandas as pd
import ccxt
import talib
import pandas_ta as ta
# from convert import DateConverter

api_client = ccxt.binance()
# conv_date = DateConverter()
class GetData:  
    
    def __init__(self, _symbol, _time_interval, _limit):
        self.symbol = _symbol
        self.time_interval = _time_interval
        self.limit = _limit
        self.df = []
        self.talib = talib
    
    def market_data(self):
          
        # Get last 10 klines of BNBUSDT at 1h interval
        candle_data = api_client.fetch_ohlcv(self.symbol, self.time_interval, limit = self.limit)
        self.df = pd.DataFrame(candle_data, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
        self.df['time'] = pd.to_datetime(self.df['time'], unit='ms')
        self.df = pd.concat([self.df, self.df.ta.rsi()], axis=1)
        self.df.to_csv('candle_data_ccxt.csv')
        # print(self.df)
        # print("<<<<<<<<<<<<<<<   D    O   N   E   >>>>>>>>>>>>>>")
        return self.df