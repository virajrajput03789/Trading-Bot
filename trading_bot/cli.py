import argparse
import os
import sys

# Ensure UTF-8 output on Windows consoles to support box-drawing characters
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from bot.client import BinanceTestnetClient, APIError
from bot.validators import validate_all
from bot.orders import place_order

def main():
    """Main CLI entry point for the trading bot."""
    parser = argparse.ArgumentParser(description="Binance Futures Testnet Trading Bot")
    parser.add_argument("--symbol", required=True, help="Trading symbol (e.g., BTCUSDT)")
    parser.add_argument("--side", required=True, help="Order side (BUY or SELL)")
    parser.add_argument("--type", required=True, help="Order type (MARKET, LIMIT, STOP_MARKET)")
    parser.add_argument("--quantity", required=True, help="Order quantity")
    parser.add_argument("--price", required=False, help="Price for LIMIT orders (limit price) or STOP_MARKET orders (stop/trigger price). Not required for MARKET.")
    parser.add_argument("--api-key", required=False, help="Binance API Key")
    parser.add_argument("--api-secret", required=False, help="Binance API Secret")
    
    args = parser.parse_args()
    
    api_key = args.api_key or os.environ.get("BINANCE_API_KEY")
    api_secret = args.api_secret or os.environ.get("BINANCE_API_SECRET")
    
    if not api_key or not api_secret:
        print("❌ Error: API key and secret must be provided via args or environment variables.")
        sys.exit(1)
        
    try:
        params = validate_all(args.symbol, args.side, args.type, args.quantity, args.price)
    except ValueError as e:
        print(f"❌ Validation Error: {e}")
        sys.exit(1)
        
    print("╔══════════════════════════════╗")
    print("║     ORDER REQUEST SUMMARY    ║")
    print("╚══════════════════════════════╝")
    print(f"Symbol   : {params['symbol']}")
    print(f"Side     : {params['side']}")
    print(f"Type     : {params['order_type']}")
    print(f"Quantity : {params['quantity']}")
    if params['price']:
        print(f"Price    : {params['price']}")
    print("\nPlacing order...\n")
    
    client = BinanceTestnetClient(api_key, api_secret)
    result = place_order(client, params)
    
    if result.get("success"):
        print("╔══════════════════════════════╗")
        print("║     ORDER RESPONSE           ║")
        print("╚══════════════════════════════╝")
        print(f"Order ID     : {result.get('orderId')}")
        print(f"Status       : {result.get('status')}")
        print(f"Executed Qty : {result.get('executedQty')}")
        print(f"Avg Price    : {result.get('avgPrice')}\n")
        print("✅ Order placed successfully!")
        sys.exit(0)
    else:
        print(f"❌ Order failed: {result.get('error')}")
        sys.exit(1)

if __name__ == "__main__":
    main()
