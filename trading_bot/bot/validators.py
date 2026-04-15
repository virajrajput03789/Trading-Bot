from typing import Optional, Dict, Any

def validate_symbol(symbol: str) -> str:
    """Validate and format the trading symbol."""
    if not symbol or not isinstance(symbol, str):
        raise ValueError("Symbol must be a non-empty string.")
    symbol = symbol.strip().upper()
    if not symbol.isalpha():
        raise ValueError("Symbol must contain only letters.")
    if len(symbol) > 20:
        raise ValueError("Symbol must be 20 characters or less.")
    return symbol

def validate_side(side: str) -> str:
    """Validate and format the order side."""
    side = side.strip().upper()
    if side not in ("BUY", "SELL"):
        raise ValueError("Side must be BUY or SELL.")
    return side

def validate_order_type(order_type: str) -> str:
    """Validate and format the order type."""
    order_type = order_type.strip().upper()
    if order_type not in ("MARKET", "LIMIT", "STOP_MARKET"):
        raise ValueError("Order type must be MARKET, LIMIT, or STOP_MARKET.")
    return order_type

def validate_quantity(quantity: str) -> float:
    """Validate and format the order quantity."""
    try:
        qty = float(quantity)
    except (ValueError, TypeError):
        raise ValueError("Quantity must be a valid number.")
    if qty <= 0:
        raise ValueError("Quantity must be a positive number.")
    return qty

def validate_price(price: Optional[str], order_type: str) -> Optional[float]:
    """Validate and format the order price based on type."""
    if order_type == "MARKET":
        if price is not None:
            raise ValueError("Price should not be provided for MARKET orders.")
        return None
        
    if price is None:
        raise ValueError(f"Price is required for {order_type} orders.")
        
    try:
        p = float(price)
    except (ValueError, TypeError):
        raise ValueError("Price must be a valid number.")
        
    if p <= 0:
        raise ValueError("Price must be a positive number.")
    return p

def validate_all(symbol: str, side: str, order_type: str, 
                 quantity: str, price: Optional[str]) -> Dict[str, Any]:
    """Run all validations and return a clean dictionary of parameters."""
    clean_symbol = validate_symbol(symbol)
    clean_side = validate_side(side)
    clean_type = validate_order_type(order_type)
    clean_qty = validate_quantity(quantity)
    clean_price = validate_price(price, clean_type)
    
    return {
        "symbol": clean_symbol,
        "side": clean_side,
        "order_type": clean_type,
        "quantity": clean_qty,
        "price": clean_price
    }
