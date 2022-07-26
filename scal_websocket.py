import pprint
import sys
import json
import datetime
import time
import websocket
from datetime import datetime as dt

import settings
import unregister
import register
import send_order_entry
import order_info
import order_info_exit
import settle_ioc_limit
import send_order_exit_market
import positions
# noinspection PyUnresolvedReferences
import scal_websocket

hasPositions = False
cur_price = 0
trade_side = 0
order_price = 0
lest_qty = 0
margin_trade_type = 3
position_interval_counter = 0


def print_with_time(message, end):
    print(str(datetime.datetime.now()) + ' ' + message, end=",")


def on_message(ws, message):
    content = json.loads(message)
    scal_websocket.cur_price = content["CurrentPrice"]
    print_with_time("curPrice:" + str(cur_price), " ")
    if cur_price is None:
        print("")
        return

    # ポジションがない場合はエントリ
    if not hasPositions:
        print("")

        scal_websocket.hasPositions = True

        prev_close = content["PreviousClose"]
        pprint.pprint("PreviousClose:" + str(prev_close))

        entry_price = 0
        if scal_websocket.trade_side == "2":
            # 買いエントリ
            # 金利がかからない一般(デイトレ)
            scal_websocket.margin_trade_type = 3
            entry_price = cur_price + 1000

        else:
            # 売りエントリ
            scal_websocket.trade_side = "1"
            # 売りエントリの場合はプレミアム料を取られるので制度信用
            scal_websocket.margin_trade_type = 1
            entry_price = cur_price - 1000

        # エントリ
        entry_order_id = send_order_entry.send_order_entry(trade_side, margin_trade_type, entry_price)

        while True:
            # 全約定するまで待つ
            scal_websocket.order_price = order_info.orders_info(entry_order_id)
            if order_price is not None:
                break
            time.sleep(0.2)

        # イクジット用ポジション数を初期化
        scal_websocket.lest_qty = settings.qty

    # ポジジョンがある場合は、利食い損切り
    else:
        print("order_price:" + str(order_price))
        now_time = dt.now()

        # すべて決済済みでない場合は利食い損切り
        if lest_qty > 0:

            exit_order_id = None
            # 買いエントリの場合
            if trade_side == "2":
                # 損切 or 時間切れ
                if cur_price <= order_price - settings.buy_stop_loss_margin or now_time > settings.exit_time:
                    exit_order_id = send_order_exit_market.send_order_exit_market(1, margin_trade_type, lest_qty)
                else:
                    # 利食い
                    if cur_price >= order_price + settings.buy_take_profit_margin:
                        exit_order_id = settle_ioc_limit.settle_ioc_limit_a(
                            1,
                            margin_trade_type,
                            lest_qty,
                            order_price + settings.buy_take_profit_margin)

            # 売りエントリの場合
            else:
                # 損切 or 時間切れ
                if cur_price >= order_price + settings.sell_stop_loss_margin or now_time > settings.exit_time:
                    exit_order_id = send_order_exit_market.send_order_exit_market(2, margin_trade_type, lest_qty)
                else:
                    # 利食い
                    if cur_price <= order_price - settings.sell_take_profit_margin:
                        exit_order_id = settle_ioc_limit.settle_ioc_limit_a(
                            2,
                            margin_trade_type,
                            lest_qty,
                            order_price - settings.sell_take_profit_margin)

            time.sleep(0.25)

            # 全約定するまで待つ
            if exit_order_id is not None:
                while True:
                    if order_info_exit.orders_info_exit(exit_order_id):
                        break
                    time.sleep(0.15)

                # ポジション数を更新
                scal_websocket.lest_qty = positions.positions_a(trade_side)

            else:
                # 他フォームから決済の場合もあるので10回に1回はポジション数を更新
                if scal_websocket.position_interval_counter > 10:
                    scal_websocket.lest_qty = positions.positions_a(trade_side)
                    scal_websocket.position_interval_counter = 0
                else:
                    scal_websocket.position_interval_counter = scal_websocket.position_interval_counter + 1

        else:
            # すべて決済済みでも最低ある程度は記録を残す
            ws.close()


def on_error(ws, error):
    pprint.pprint('--- ERROR --- ')
    pprint.pprint(error)


def on_close(ws):
    pprint.pprint('--- DISCONNECTED --- ')


def on_open(ws):
    pprint.pprint(scal_websocket.trade_side)
    pprint.pprint('--- CONNECTED --- ')


def trade_start(param_side):
    # 初期化
    scal_websocket.hasPositions = False
    scal_websocket.cur_price = 0
    scal_websocket.trade_side = 0
    scal_websocket.order_price = 0
    scal_websocket.lest_qty = 0
    scal_websocket.margin_trade_type = 3
    scal_websocket.position_interval_counter = 0

    # 引数から売りか買いかを取得
    scal_websocket.trade_side = param_side

    unregister.unregister()
    register.register()
    print('--- webSocket Start--- ')
    url = 'ws://localhost:' + settings.port + '/kabusapi/websocket'
    # websocket.enableTrace(True)
    ws_client = websocket.WebSocketApp(url,
                                       on_message=on_message,
                                       on_error=on_error,
                                       on_close=on_close)
    ws_client.on_open = on_open

    ws_client.run_forever()

    pprint.pprint('--- websocket_exit --- ')


if __name__ == '__main__':
    side = sys.argv[1]
    trade_start(side)
