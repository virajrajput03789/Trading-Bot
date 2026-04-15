# Binance Futures Testnet Trading Bot

A production-quality command-line trading bot for the Binance Futures Testnet. It provides a simple CLI to place `MARKET`, `LIMIT`, and `STOP_MARKET` orders, built with strict validation, detailed logging, and a robust client architecture.

## Prerequisites

- Python 3.9 or higher
- `pip` (Python package installer)

## Setup Steps

1. **Clone / unzip the repository:**
   ```bash
   git clone <repository_url>
   cd trading_bot
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables:**
   You need Binance Futures Testnet credentials. Get them by logging into [https://testnet.binancefuture.com](https://testnet.binancefuture.com).
   ```bash
   export BINANCE_API_KEY="your_testnet_api_key"
   export BINANCE_API_SECRET="your_testnet_api_secret"
   ```
   *On Windows (PowerShell):*
   ```powershell
   $env:BINANCE_API_KEY="your_testnet_api_key"
   $env:BINANCE_API_SECRET="your_testnet_api_secret"
   ```

## How to Run

- **MARKET BUY example:**
  ```bash
  python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
  ```

- **LIMIT SELL example:**
  ```bash
  python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 50000.0
  ```

- **STOP_MARKET SELL example (triggers when price drops to X):**
  ```bash
  python cli.py --symbol BTCUSDT --side SELL --type STOP_MARKET \
  --quantity 0.003 --price 45000.0
  ```
  > Note: For STOP_MARKET, `--price` is used as the `stopPrice` 
  > (trigger price). The order executes as a market order when 
  > the price reaches this level.

## Sample Output

```
╔══════════════════════════════╗
║     ORDER REQUEST SUMMARY    ║
╚══════════════════════════════╝
Symbol   : BTCUSDT
Side     : BUY
Type     : LIMIT
Quantity : 0.001
Price    : 30000.0

Placing order...

╔══════════════════════════════╗
║     ORDER RESPONSE           ║
╚══════════════════════════════╝
Order ID     : 123456789
Status       : NEW
Executed Qty : 0.0
Avg Price    : 0.0

✅ Order placed successfully!
```

## Log File Location

The bot logs its activity to `trading_bot.log` in the root directory. 
- It captures `INFO` level events (like order placement attempts and success/failure).
- It captures `DEBUG` level events (like raw request URLs, parameters without secrets, and raw API responses).
The log file automatically rotates up to 5 backups, with a max size of 10MB each.

## Assumptions

- Uses the **USDT-M** futures testnet (`https://testnet.binancefuture.com`).
- Assumes the account has sufficient balance and leverage set up for the orders.
- Only tested with typical USDT pairs (e.g., `BTCUSDT`, `ETHUSDT`).
- STOP_MARKET orders use Binance's standard `/fapi/v1/order` endpoint with `stopPrice` parameter (not the Algo Order API).
- Minimum order notional value must be at least 100 USDT (e.g., for BTCUSDT at ~84000, minimum quantity is ~0.002).

## Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py
│   ├── logging_config.py
│   ├── orders.py
│   └── validators.py
├── cli.py
├── README.md
├── test_algo.py          # development test script
└── requirements.txt
```

## Additional Files

### test_algo.py
A standalone test script used during development to verify the STOP_MARKET algo order endpoint behavior on the testnet. Not required for normal bot usage.
