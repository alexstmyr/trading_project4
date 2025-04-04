import hashlib
import hmac

import requests
import time

from urllib.parse import urlencode
from models import Trades


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

        elif method == 'POST':
            return requests.post(f"{self.base_url}{endpoint}", params=params, headers=headers)

    # ping for binance (api/v3/ping)
    def ping(self) -> bool:
        #res = self._execute_request(endpoint = "/v3/ping", params = {})
        res = requests.get(self.base_url + "/v3/ping")
        #print(res.status_code)
        #print(res.text)
        return res.status_code == 200

    def get_price(self, symbol: str):
        # res = self._execute_request(endpoint: "/v3/ticker/price", paramas: {"symbol": symbol})
        res = requests.get(self.base_url + f"/v3/ticker/price?symbol={symbol}")
        if res.status_code == 200:
            return res.json()
        raise Exception(f'Error fetching price: {res.text}')
    
    def get_account_info(self):
        res = self._execute_request('/v3/account', {}, 'GET')
        if res.status_code == 200:
            return res.json()
        raise Exception(f'Error fetching account info: {res.text}')
    
    def get_price_history(self, symbol: str, interval: str = "1h", limit: int = 100):
        url = f"https://testnet.binance.vision/api/v3/klines"
        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit
        }
        res = requests.get(url, params=params)
        if res.status_code == 200:
            return res.json()
        raise Exception(f"Error fetching price history: {res.text}")

    
    def place_order(self, symbol: str, side: str, order_type: str, quantity: float, test: bool = True):
        endpoint = "/v3/order/test" if test else "/v3/order"
        params = {
            'symbol': symbol,
            'side': side.upper(),
            'type': order_type.upper(),
            'quantity': quantity
        }
        res = self._execute_request(endpoint, params, method='POST')

        if res.status_code == 200:
            return res.json()
        raise Exception(f'Error placing order: {res.text}')
    
    def get_trades(self, symbol: str) -> list[Trades]:
        res = self._execute_request(endpoint= "/v3/myTrades", params= {"symbol": symbol})
        trades = Trades.parse_obj(res.json())
        print(res.status_code)
        print(res.json())
        return trades