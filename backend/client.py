import hashlib
import hmac

import requests
import time

from urllib.parse import urlencode


class BinanceTestClient:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = 'https://testnet.binance.vision/api'

    def _generate_signature(self, query_string: str) -> str:
        return hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def _execute_request(self, endpoint: str, params: dict, method: str = 'GET'):
        timestamp = int(time.time() * 1000)
        params['timestamp'] = timestamp

        query_string = urlencode(params)
        signature = self._generate_signature(query_string)
        params['signature'] = signature

        headers = {
            'X-MBX-APIKEY': self.api_key
        }

        if method == 'GET':
            return requests.get(f"{self.base_url}{endpoint}", params=params, headers=headers)

        return requests.post(f"{self.base_url}{endpoint}", params=params, headers=headers)

    # ping for binance (api/v3/ping)
    def ping(self) -> bool:
        #res = self._execute_request(endpoint = "/v3/ping", params = {})
        request.get(self.base_url + "/v3/ping")
        #print(res.status_code)
        #print(res.text)

    def get_price(self, symbol: str):
        # res = self._execute_request(endpoint: "/v3/ticker/price", paramas: {"symbol": symbol})
        request.get(self.base_url + "/v3/ticker/price?symbol={}".format(symbol))
        print(res.status_code)
        print(res.text)
    
    def get_trades(self, symbol: str) -> list[Trades]:
        res = self._execute_request(endpoint= "/v3/myTrades", params= {"symbol": symbol})
        trades = Trades.parse_obj(res.json())
        print(res.status_code)
        print(res.json())
        return trades