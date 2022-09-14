import talib
import pandas as pd
df = pd.read_csv('update_data_1m_minute.csv')
buy_price = 0
def profit_margin(buy, sell):
    gross_profit = sell - buy
    profit_by_revenue = gross_profit / sell

    percentage = profit_by_revenue * 100
    return percentage
for i in range(100):
    print(i, profit_margin(df['close'][i], df['close'][i+1]))
c = 0
# for i in range(len(df['close']) - 5):
#     # if (talib.CDL3INSIDE(df['open'], df['high'], df['low'], df['close']))[i] == 100:
#     #     print(i)
#     if df['close'][i] < df['close'][ i + 1] < df['close'][i + 2] < df['close'][i + 3] and profit_margin(float(df['high'][i+3]), float(df['close'][i+4])) > 0.4:
#         print(profit_margin(float(df['high'][i+3]), float(df['close'][i+4])))
     
#         c = c + 1
        
print(f'c : {c}')        # print(df['close'][i], df['close'][ i + 1], df['close'][i + 2])
# integer = CDL3INSIDE(open, high, low, close)