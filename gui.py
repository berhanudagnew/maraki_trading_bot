import tkinter as tk
from tkinter import ttk
import ccxt
# from trader import trader
from test_class import test
from secret import API_KEY, SECRET_KEY, USER_ID
import multiprocessing

window = tk.Tk()
window.title("M    A    R    A   K   I")
window.call("source", "azure.tcl")
window.call("set_theme", "light")

global process


def start():
    '''
        Start and stop a trader instance using multiprocessing
    '''
    if btn_start['text'] == 'Start':
        # Getting parameters from user input
        global process
        symbol = ent_symbol.get()
        timeframe = timeframe_option.get()
        exchange = exchange_option.get()
        quantity = float(ent_quantity.get())
        isFutures = chkbtn_isFuture.instate(['selected'])
        isLive = chkbtn_isLive.instate(['selected'])
        # api_key = ent_apiKey.get()
        api_key = API_KEY
        # secret_key = ent_apiSecret.get()
        secret_key = SECRET_KEY
        # user_id = ent_userId.get().split(',')
        user_id = USER_ID

        # Print input parameters for checking
        print(symbol, timeframe, 
            exchange, quantity, 
            isFutures, isLive, 
            api_key, secret_key, 
            user_id)
        print

        # Initialize a trader intance on another process,
        # to avoid blocking Tkinter's main loop
        # main = trader(symbol, timeframe, exchange, quantity, isFutures, isLive, api_key, secret_key, user_id)
        process = multiprocessing.Process(target = main.run)
        process.start()
        btn_start['text'] = 'Stop'
        lbl_status['text'] = 'Status: Running'
        lbl_status['foreground'] = 'green'

    elif btn_start['text'] == 'Stop':
        # Terminate trader instance, change status labal
        print('Stoped')
        process.terminate()
        btn_start['text'] = 'Start'
        lbl_status['text'] = 'Status: Stopped'
        lbl_status['foreground'] = 'red'

if __name__ == '__main__':
    # Title
    lbl_title = ttk.Label(master = window, text = "M    A    R    A   K   I", font = ("Helvetica",30))
    lbl_title.grid(row = 0, column = 0, columnspan = 2, padx = 10, pady = 10)

    # Status
    lbl_status = ttk.Label(master = window, text = 'Status: Stopped', foreground = 'red', font = (20))
    lbl_status.grid(row = 1, column = 0, padx = 10, pady = 10)

    # Mode button
    ##  chkbtn_mode = ttk.Checkbutton(master = window, text = 'Dark mode', style = 'Switch.TCheckbutton', command = toggleMode)
    ## chkbtn_mode.grid(row = 1, column = 1, padx = 10, pady = 10)

    # Symbol entry
    frm_symbol = ttk.Frame(master = window)
    ent_symbol = ttk.Entry(master = frm_symbol, width = 10)
    lbl_symbol = ttk.Label(master = frm_symbol, text = "Enter pair symbol")
    ent_symbol.grid(row = 0, column = 1, padx = 10)
    lbl_symbol.grid(row = 0, column = 0)
    frm_symbol.grid(row = 2, column = 0, padx = 10, pady = 10, sticky = "w")

    # Timeframe list
    frm_timeframe = ttk.Frame(master = window)
    timeframe_list = ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M']
    timeframe_option = tk.StringVar(master = window)
    lbl_timeframe = ttk.Label(master = frm_timeframe, text = 'Choose timeframe')
    timeframe_option.set(timeframe_list[0])
    w = ttk.OptionMenu(frm_timeframe, timeframe_option, timeframe_list[0], *timeframe_list)
    w.grid(row = 0, column = 1, padx = 10, pady = 10, sticky = 'w')
    lbl_timeframe.grid(row = 0, column = 0)
    frm_timeframe.grid(row = 3, column = 0, padx = 10, pady = 10, sticky = "w")

    # Exchange list
    frm_exchange = ttk.Frame(master = window)
    exchange_list = ccxt.exchanges # Check CCXT available exchanges
    exchange_option = tk.StringVar(master = window)
    lbl_exchange = ttk.Label(master = frm_exchange, text = 'Choose exchange')
    exchange_option.set(exchange_list[0])
    w = ttk.OptionMenu(frm_exchange, exchange_option, exchange_list[0], *exchange_list)
    w.grid(row = 0, column = 1, padx = 10, pady = 10, sticky = 'w')
    lbl_exchange.grid(row = 0, column = 0)
    frm_exchange.grid(row = 4, column = 0,  padx = 10, pady = 10, sticky = 'w')

    # Quantity entry
    frm_quantity = ttk.Frame(master = window)
    ent_quantity = ttk.Entry(master = frm_quantity, width = 10)
    lbl_quantity = ttk.Label(master = frm_quantity, text = "Enter trade quantity")
    ent_quantity.grid(row = 0, column = 1, padx = 10)
    lbl_quantity.grid(row = 0, column = 0)
    frm_quantity.grid(row = 2, column = 1, padx = 10, pady = 10, sticky = "w")

    # Is_future checkbox
    frm_isFuture = ttk.Frame(master = window)
    chkbtn_isFuture = ttk.Checkbutton(master = frm_isFuture)
    lbl_isFuture = ttk.Label(master = frm_isFuture, text = "Trading futures?", takefocus = 0)
    chkbtn_isFuture.grid(row = 0, column = 1)
    lbl_isFuture.grid(row = 0, column = 0)
    frm_isFuture.grid(row = 3, column = 1, padx = 10, pady = 10, sticky = "w")

    # Live_trade checkbox
    frm_isLive = ttk.Frame(master = window)
    chkbtn_isLive = ttk.Checkbutton(master = frm_isLive)
    lbl_isLive = ttk.Label(master = frm_isLive, text = "Trading live?", takefocus = 0)
    chkbtn_isLive.grid(row = 0, column = 1)
    lbl_isLive.grid(row = 0, column = 0)
    frm_isLive.grid(row = 4, column = 1, padx = 10, pady = 10, sticky = "w")

    # # API key entry
    # frm_apiKey = ttk.Frame(master = window)
    # ent_apiKey = ttk.Entry(master = frm_apiKey, width = 60)
    # lbl_apiKey = ttk.Label(master = frm_apiKey, text = "Enter API key   ")
    # ent_apiKey.grid(row = 1, column = 0)
    # lbl_apiKey.grid(row = 0, column = 0)
    # frm_apiKey.grid(row = 5, column = 0, columnspan = 2, padx = 10, pady = 10)

    # # API secret entry
    # frm_apiSecret = ttk.Frame(master = window)
    # ent_apiSecret = ttk.Entry(master = frm_apiSecret, width = 60)
    # lbl_apiSecret = ttk.Label(master = frm_apiSecret, text = "Enter API secret")
    # ent_apiSecret.grid(row = 1, column = 0)
    # lbl_apiSecret.grid(row = 0, column = 0)
    # frm_apiSecret.grid(row = 6, column = 0, columnspan = 2, padx = 10, pady = 10)

    # # User IDs entry
    # frm_userId = ttk.Frame(master = window)
    # ent_userId = ttk.Entry(master = frm_userId, width = 60)
    # lbl_userId = ttk.Label(master = frm_userId, text = "Enter Telegram user IDs (seperate by commas)")
    # ent_userId.grid(row = 1, column = 0, padx = 10)
    # lbl_userId.grid(row = 0, column = 0)
    # frm_userId.grid(row = 7, column = 0, columnspan = 2, padx = 10, pady = 10)

    # Start button
    btn_start = ttk.Button(master = window, text = 'Start', command = start)
    btn_start.grid(row = 8, column = 0, columnspan = 2, padx = 10, pady = 10)

    window.mainloop()