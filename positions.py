import urllib.request
import urllib.error
import urllib.parse
import json
import pprint
import settings
import sys


def positions_a(side):
    url = 'http://localhost:' + settings.port + '/kabusapi/positions'
    params = {'product': 0, 'symbol': settings.symbol, 'side': side}
    req = urllib.request.Request('{}?{}'.format(url, urllib.parse.urlencode(params)), method='GET')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-API-KEY', settings.token)

    try:
        print('###positions')
        with urllib.request.urlopen(req) as res:
            print(res.status, res.reason)
            for header in res.getheaders():
                print(header)
            print()
            res_json = res.read()
            content = json.loads(res_json)
            pprint.pprint(content)
            leaves_qty = 0
            for position in content:
                # 残ポジション数
                leaves_qty = leaves_qty + position['LeavesQty']

            # ポジション数を返す

            return leaves_qty

    except urllib.error.HTTPError as e:
        print(e)
        content = json.loads(e.read())
        pprint.pprint(content)
    except Exception as e:
        print(e)

    sys.exit()
