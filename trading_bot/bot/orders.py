from bot.client import BinanceTestnetClient, APIError
from bot.logging_config import get_logger

logger = get_logger("orders")

def place_order(client: BinanceTestnetClient, params: dict) -> dict:
    """Execute order placement using validated parameters."""
    symbol = params["symbol"]
    side = params["side"]
    order_type = params["order_type"]
    qty = params["quantity"]
    price = params["price"]
    
    logger.info(f"Attempting to place {order_type} {side} order for {qty} {symbol}")
    
    try:
        if order_type == "STOP_MARKET":
            resp = client.place_order(symbol, side, order_type, qty, stop_price=price)
        else:
            resp = client.place_order(symbol, side, order_type, qty, price=price)
            
        result = {
            "orderId": resp.get("orderId"),
            "symbol": resp.get("symbol", symbol),
            "side": resp.get("side", side),
            "type": resp.get("type", order_type),
            "origQty": resp.get("origQty", qty),
            "executedQty": resp.get("executedQty", "0.0"),
            "avgPrice": resp.get("avgPrice", "0.0"),
            "status": resp.get("status", "NEW"),
            "success": True,
            "raw_response": resp
        }
        
        logger.info(
            f"Order placed successfully | orderId={result['orderId']} "
            f"status={result['status']} symbol={result['symbol']} "
            f"side={result['side']} type={result['type']} qty={result['origQty']}"
        )
        return result
        
    except APIError as e:
        logger.error(f"API Error placing order: {e.status_code} - {e.response_body}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"Unexpected error placing order: {e}")
        return {"success": False, "error": str(e)}
