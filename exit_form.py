import tkinter
import send_order_exit_market
import settings


# click時のイベント
def btn_buy_entry_exit_click():
    send_order_exit_market.send_order_exit_market(1, 3, settings.qty)


def btn_sell_entry_exit_click():
    send_order_exit_market.send_order_exit_market(2, 1, settings.qty)


# 画面作成
tkTrade = tkinter.Tk()
tkTrade.geometry('300x200')  # 画面サイズの設定
tkTrade.title('決済')  # 画面タイトルの設定

# ボタンの作成
btnBuy = tkinter.Button(tkTrade, text='買いエントリイクジット', command=btn_buy_entry_exit_click)
btnSell = tkinter.Button(tkTrade, text='売りエントリイクジット', command=btn_sell_entry_exit_click)
btnBuy.place(x=10, y=50)  # ボタンを配置する位置の設定
btnSell.place(x=175, y=50)  # ボタンを配置する位置の設定

# 画面をそのまま表示
tkTrade.mainloop()
