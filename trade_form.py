import scal_websocket
import settings
from tkinter import *
from tkinter import ttk

# 画面作成
tkTrade = Tk()
tkTrade.geometry('300x250')  # 画面サイズの設定
tkTrade.title('scal')  # 画面タイトルの設定

frame0 = ttk.Frame(tkTrade, padding=(10, 20, 10, 10))
frame0.grid()

label0 = ttk.Label(frame0, text='建玉数', padding=(5, 10, 5, 10))
label0.grid(row=0, column=0, sticky=E)

# 建玉数入力
positions = IntVar()
positions.set(settings.qty)
positions_entry = ttk.Entry(
    frame0,
    textvariable=positions,
    width=5,
    justify=RIGHT)
positions_entry.grid(row=0, column=1, sticky=W)

tkTrade.resizable(False, False)
frame1 = ttk.Frame(tkTrade, padding=(10, 10, 10, 32))
frame1.grid()

label1 = ttk.Label(frame1, text='買いTakeProfit', padding=(5, 10, 5, 10))
label1.grid(row=0, column=0, sticky=E)

# 買い利食い幅入力
buy_take_profit = IntVar()
buy_take_profit.set(settings.buy_take_profit_margin)
buy_take_profit_entry = ttk.Entry(
    frame1,
    textvariable=buy_take_profit,
    width=5,
    justify=RIGHT)
buy_take_profit_entry.grid(row=0, column=1, sticky=W)

label2 = ttk.Label(frame1, text='買いStopLoss', padding=(5, 10, 5, 10))
label2.grid(row=1, column=0, sticky=E)

# 買い損切幅入力
buy_stop_loss = IntVar()
buy_stop_loss.set(settings.buy_stop_loss_margin)
buy_stop_loss_entry = ttk.Entry(
    frame1,
    textvariable=buy_stop_loss,
    width=5,
    justify=RIGHT)
buy_stop_loss_entry.grid(row=1, column=1, sticky=W)

label3 = ttk.Label(frame1, text='売りTakeProfit', padding=(20, 10, 5, 10))
label3.grid(row=0, column=3, sticky=E)

# 売り利食い幅入力
sell_take_profit = IntVar()
sell_take_profit.set(settings.buy_take_profit_margin)
sell_take_profit_entry = ttk.Entry(
    frame1,
    textvariable=sell_take_profit,
    width=5,
    justify=RIGHT)
sell_take_profit_entry.grid(row=0, column=4, sticky=W)

label4 = ttk.Label(frame1, text='売りStopLoss', padding=(20, 10, 5, 10))
label4.grid(row=1, column=3, sticky=E)

# 売り損切幅入力
sell_stop_loss = IntVar()
sell_stop_loss.set(settings.sell_stop_loss_margin)
sell_stop_loss_entry = ttk.Entry(
    frame1,
    textvariable=sell_stop_loss,
    width=5,
    justify=RIGHT)
sell_stop_loss_entry.grid(row=1, column=4, sticky=W)


# click時のイベント
def btn_buy_click():
    settings.qty = positions.get()
    settings.buy_take_profit_margin = buy_take_profit.get()
    settings.buy_stop_loss_margin = buy_stop_loss.get()
    scal_websocket.trade_start("2")


def btn_sell_click():
    settings.qty = positions.get()
    settings.sell_take_profit_margin = sell_take_profit.get()
    settings.sell_stop_loss_margin = sell_stop_loss.get()
    scal_websocket.trade_start("1")


# ボタン
frame2 = ttk.Frame(tkTrade, padding=0)
frame2.grid()
btnBuy = ttk.Button(
    frame2, text='買い',
    command=btn_buy_click)
btnBuy.grid(row=0, column=0, columnspan=2, sticky=E)
frame2.grid_columnconfigure(3, minsize=50)
btnSell = ttk.Button(
    frame2, text='売り',
    command=btn_sell_click)
btnSell.grid(row=0, column=5, columnspan=2, sticky=E)

# 画面をそのまま表示
tkTrade.mainloop()
