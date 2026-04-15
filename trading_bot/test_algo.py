import os
import sys
import requests
import time
import hmac
import hashlib
from urllib.parse import urlencode

api_key = "dummy"
api_secret = "dummy"

def _generate_signature(secret, query_string):
    return hmac.new(
        secret.encode('utf-8'),
        query_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

def send_request(endpoint, params):
    params['timestamp'] = int(time.time() * 1000)
    query_string = urlencode(params)
    signature = _generate_signature(api_secret, query_string)
    params['signature'] = signature
    
    url = f"https://testnet.binancefuture.com{endpoint}"
    headers = {
        "X-MBX-APIKEY": api_key,
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, params=params)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")

print("Testing /fapi/v1/nonExistent...")
send_request("/fapi/v1/nonExistent", {
    "symbol": "BTCUSDT",
    "side": "SELL",
    "type": "STOP_MARKET",
    "quantity": 0.001,
    "triggerPrice": 45000.0,
    "algoType": "CONDITIONAL"
})

print("Testing /fapi/v1/algoOrder with stopPrice...")
send_request("/fapi/v1/algoOrder", {
    "symbol": "BTCUSDT",
    "side": "SELL",
    "type": "STOP_MARKET",
    "quantity": 0.001,
    "stopPrice": 45000.0,
    "algoType": "CONDITIONAL"
})
