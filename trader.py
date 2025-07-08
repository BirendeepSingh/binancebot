from binance.client import Client
from binance.enums import *
from logger_config import setup_logger

class BasicBot:
    def get_order_history(self, symbol, limit=10):
        try:
            orders = self.client.futures_get_all_orders(symbol=symbol.upper(), limit=limit)
            if not orders:
                print("📭 No recent orders found.")
                return []

            recent_orders = []
            for order in orders:
                recent_orders.append({
                    'symbol': order['symbol'],
                    'side': order['side'],
                    'type': order['type'],
                    'status': order['status'],
                    'price': order['price'],
                    'origQty': order['origQty'],
                    'executedQty': order['executedQty'],
                    'time': order['updateTime']
                })
            self.logger.info(f"Fetched {len(recent_orders)} orders for {symbol.upper()}")
            return recent_orders

        except Exception as e:
            self.logger.error(f"Error fetching order history for {symbol}: {str(e)}")
            return []

    def get_balance(self, asset='USDT'):
        try:
            balances = self.client.futures_account_balance()
            for entry in balances:
                if entry['asset'] == asset:
                    balance = float(entry['balance'])
                    available = float(entry['availableBalance'])
                    self.logger.info(f"{asset} Balance: Total = {balance}, Available = {available}")
                    return balance, available
            return 0.0, 0.0
        except Exception as e:
            self.logger.error(f"Error fetching balance: {str(e)}")
            return 0.0, 0.0

    def get_open_positions(self):
        try:
            positions = self.client.futures_position_information()
            open_positions = [pos for pos in positions if float(pos['positionAmt']) != 0.0]
            for pos in open_positions:
                symbol = pos['symbol']
                amt = float(pos['positionAmt'])
                entry_price = float(pos['entryPrice'])
                unrealized_pnl = float(pos['unrealizedProfit'])
                self.logger.info(f"{symbol}: Amt={amt}, Entry={entry_price}, PnL={unrealized_pnl}")
            return open_positions
        except Exception as e:
            self.logger.error(f"Error fetching open positions: {str(e)}")
            return []

    def get_mark_price(self, symbol):
        try:
            price_info = self.client.futures_mark_price(symbol=symbol.upper())
            mark_price = float(price_info['markPrice'])
            self.logger.info(f"Mark price for {symbol.upper()}: {mark_price}")
            return mark_price
        except Exception as e:
            self.logger.error(f"Error fetching mark price for {symbol}: {str(e)}")
            return None

    def __init__(self, api_key, api_secret, testnet=True):
        self.logger = setup_logger()
        self.client = Client(api_key, api_secret)

        if testnet:
            self.client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'
            self.logger.info("Using Binance Futures Testnet")

    def place_order(self, symbol, side, order_type, quantity, price=None, stop_price=None):
        try:
            side_enum = SIDE_BUY if side.lower() == 'buy' else SIDE_SELL

            # Base order object
            order_data = {
                'symbol': symbol.upper(),
                'side': side_enum,
                'type': order_type.upper(),
                'quantity': quantity
            }

            # Handle LIMIT orders
            if order_type.lower() == 'limit':
                order_data['price'] = price
                order_data['timeInForce'] = TIME_IN_FORCE_GTC

            # Handle STOP_MARKET or STOP_LIMIT
            elif order_type.lower() in ['stop_market', 'stop_limit']:
                order_data['stopPrice'] = stop_price
                if order_type.lower() == 'stop_limit':
                    order_data['price'] = price
                    order_data['timeInForce'] = TIME_IN_FORCE_GTC

            self.logger.info(f"Placing order: {order_data}")
            order = self.client.futures_create_order(**order_data)
            self.logger.info(f"Order placed: {order}")
            return order

        except Exception as e:
            self.logger.error(f"Error placing order: {str(e)}")
            return None