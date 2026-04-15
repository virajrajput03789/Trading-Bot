import hmac
import hashlib
import time
import requests
import json
from urllib.parse import urlencode
from bot.logging_config import get_logger

logger = get_logger("client")

class APIError(Exception):
    """Custom exception for API errors."""
    def __init__(self, message: str, status_code: int, response_body: str):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body

class BinanceTestnetClient:
    """Client for Binance Futures Testnet API."""
    BASE_URL = "https://testnet.binancefuture.com"
    
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key,
            "Content-Type": "application/json"
        })
        
    def _generate_signature(self, query_string: str) -> str:
        """Generate HMAC-SHA256 signature for API requests."""
        return hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
    def _request(self, method: str, endpoint: str, params: dict = None) -> dict:
        """Send a signed HTTP request to the Binance API."""
        if params is None:
            params = {}
            
        params['timestamp'] = int(time.time() * 1000)
        query_string = urlencode(params)
        signature = self._generate_signature(query_string)
        params['signature'] = signature
        
        url = f"{self.BASE_URL}{endpoint}"
        log_params = {k: v for k, v in params.items() if k != 'signature'}
        logger.debug(f"Sending {method} to {endpoint} | params: {log_params}")
        
        try:
            response = self.session.request(method, url, params=params)
            logger.debug(f"Response {response.status_code}: {response.text}")
            
            if not response.ok:
                raise APIError(f"API request failed: {response.reason}", 
                               response.status_code, response.text)
                               
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error during request: {e}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON response: {e}")
            raise

    def place_order(self, symbol: str, side: str, order_type: str, 
                    quantity: float, price: float = None, 
                    stop_price: float = None, time_in_force: str = "GTC") -> dict:
        """Place a new order on the futures testnet."""
        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity
        }
        
        endpoint = "/fapi/v1/order"
        
        if order_type == "LIMIT" and price is not None:
            params["price"] = price
            params["timeInForce"] = time_in_force
        elif order_type == "STOP_MARKET" and stop_price is not None:
            params["stopPrice"] = stop_price
            
        return self._request("POST", endpoint, params)
        
    def get_account_info(self) -> dict:
        """Retrieve account information and balances."""
        return self._request("GET", "/fapi/v2/account")
