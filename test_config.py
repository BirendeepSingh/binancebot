from binance.client import Client

client = Client("YOUR_KEY", "YOUR_SECRET")
client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"

print(client.futures_account_balance())
