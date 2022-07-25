import tkinter
import scal_websocket


# click時のイベント
def btn_buy_click():
    scal_websocket.trade_start("2")


def btn_sell_click():
    scal_websocket.trade_start("1")


# 画面作成
tkTrade = tkinter.Tk()
tkTrade.geometry('300x200')  # 画面サイズの設定
tkTrade.title('scal')  # 画面タイトルの設定

# ボタンの作成
btnBuy = tkinter.Button(tkTrade, text='買い', command=btn_buy_click)
btnSell = tkinter.Button(tkTrade, text='売り', command=btn_sell_click)
btnBuy.place(x=75, y=50)  # ボタンを配置する位置の設定
btnSell.place(x=200, y=50)  # ボタンを配置する位置の設定

# 画面をそのまま表示
tkTrade.mainloop()
