import json
from trader import BasicBot

def get_user_input_with_symbol(symbol):
    side = input("Enter side (buy/sell): ").lower()
    order_type = input("Enter order type (market/limit/stop_market/stop_limit): ").lower()
    quantity = float(input("Enter quantity: "))

    price = None
    stop_price = None

    if order_type == 'limit' or order_type == 'stop_limit':
        price = float(input("Enter limit price: "))

    if order_type == 'stop_market' or order_type == 'stop_limit':
        stop_price = float(input("Enter stop price: "))

    return symbol, side, order_type, quantity, price, stop_price



if __name__ == "__main__":
    with open("config.json") as f:
        config = json.load(f)

    bot = BasicBot(config["api_key"], config["api_secret"], testnet=True)

    # Show Balance
balance, available = bot.get_balance()
print(f"💰 USDT Balance: Total = {balance}, Available = {available}")

# Show open positions
positions = bot.get_open_positions()
if positions:
    print("\n📊 Open Positions:")
    for pos in positions:
        print(f"- {pos['symbol']}: Qty = {pos['positionAmt']}, Entry = {pos['entryPrice']}, PnL = {pos['unrealizedProfit']}")
else:
    print("📭 No open positions.")

    symbol = input("Enter trading pair (e.g., BTCUSDT): ")
live_price = bot.get_mark_price(symbol)

if live_price:
    print(f"📈 Current Mark Price of {symbol.upper()}: {live_price}")
else:
    print(f"⚠️ Could not fetch live price for {symbol.upper()}")

    # Show order history
orders = bot.get_order_history(symbol)
if orders:
    print(f"\n📜 Last {len(orders)} orders for {symbol.upper()}:")
    for o in orders:
        print(f"- [{o['status']}] {o['side']} {o['type']} {o['origQty']} @ {o['price']} (Executed: {o['executedQty']})")
else:
    print("📭 No recent orders found.")



    symbol, side, order_type, quantity, price, stop_price = get_user_input_with_symbol(symbol)

result = bot.place_order(symbol, side, order_type, quantity, price, stop_price)

if result:
    print("Order placed successfully!")
    print(f"Order ID: {result['orderId']}")
    print(f"Status: {result['status']}")
else:
    print("Failed to place order.")
