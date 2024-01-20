import hashlib
import hmac
import time
import requests

class Binance_API():
    api_url = "https://fapi.binance.com"
    api_key = None
    secret_key = None

    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key

    def genSignature(self, params):
        param_str = '&'.join([f'{k}={v}' for k, v in params.items()])
        hash = hmac.new(bytes(self.secret_key, "utf-8"), param_str.encode("utf-8"), hashlib.sha256)

        return hash.hexdigest()

    def HTTP_Request(self, endPoint, method, params):
        header = {
            "X-MBX-APIKEY": self.api_key
        }

        params["timestamp"] = int(time.time() * 1000)
        params["signature"] = self.genSignature(params)

        if method == "GET":
            response = requests.get(url=self.api_url + endPoint, params=params, headers=header)
        elif method == "POST":
            response = requests.post(url=self.api_url + endPoint, params=params, headers=header)
            print(response.text)

        return response.json()

    def get_candles_with_data(self, symbol, interval, startTime, endTime, limit=1440):
        endpoint = "/fapi/v1/klines"
        method = "GET"
        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit,
            "startTime": startTime,
            "endTime": endTime
        }
        return self.HTTP_Request(endPoint=endpoint, method=method, params=params)


