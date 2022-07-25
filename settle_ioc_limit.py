import urllib.request
import urllib.error
import json
import pprint
import settings
import password
import sys


# 利食いor損切り指値決済注文
def settle_ioc_limit_a(side, marginTradeType, qty, price):
    obj = {'Password': password.password,
           'Symbol': settings.symbol,
           'Exchange': 1,
           'SecurityType': 1,
           'Side': side,
           'CashMargin': 3,
           'MarginTradeType': marginTradeType,
           'DelivType': 2,
           'AccountType': 4,
           'Qty': qty,
           'ClosePositionOrder': 0,
           'Price': price,
           'ExpireDay': 0,
           'FrontOrderType': 27}
    json_data = json.dumps(obj).encode('utf-8')

    url = 'http://localhost:' + settings.port + '/kabusapi/sendorder'
    req = urllib.request.Request(url, json_data, method='POST')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-API-KEY', settings.token)

    try:
        print('###settle_ioc_limit')
        with urllib.request.urlopen(req) as res:
            print(res.status, res.reason)
            for header in res.getheaders():
                print(header)
            print()
            content = json.loads(res.read())
            pprint.pprint(content)
            # 注文ID
            order_id = content['OrderId']

            return order_id

    except urllib.error.HTTPError as e:
        print(e)
        content = json.loads(e.read())
        pprint.pprint(content)
        # 決済内容に誤りがあります はポジション取得遅延のせいなので無視
        if content['Code'] == 8:
            return

    except Exception as e:
        print(e)

    sys.exit()


# if __name__ == "__main__":
#     import sys
#
#     tradeP = settings.TradeC.TradeC("test")
#     settle_now_a(tradeP)
