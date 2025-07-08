import streamlit as st
import json
from trader import BasicBot

# Load config
with open("config.json") as f:
    config = json.load(f)

# Initialize bot
bot = BasicBot(config["api_key"], config["api_secret"], testnet=True)

st.set_page_config(page_title="Binance Testnet Bot", layout="centered")
st.title("📈 Binance Futures Testnet Bot")

# ------------------------------
# SYMBOL INPUT AND LIVE DATA
# ------------------------------
symbol = st.text_input("Enter trading pair", value="BTCUSDT").upper()

if symbol:
    # 📈 Live price
    price = bot.get_mark_price(symbol)
    if price:
        st.info(f"📉 Current Mark Price of {symbol}: `{price}`")
    
    # 💰 Balance
    balance, available = bot.get_balance()
    st.success(f"💰 USDT Balance: `{available}` available / `{balance}` total")

    # 📊 Open Positions
    positions = bot.get_open_positions()
    if positions:
        st.markdown("### 📊 Open Positions")
        for pos in positions:
            st.write(f"- {pos['symbol']}: Qty = {pos['positionAmt']}, Entry = {pos['entryPrice']}, PnL = {pos['unrealizedProfit']}")
    else:
        st.markdown("📭 No open positions.")

    # 🧾 Order History
    orders = bot.get_order_history(symbol)
    if orders:
        st.markdown("### 🧾 Recent Orders")
        for o in orders[:5]:  # show latest 5
            st.write(f"[{o['status']}] {o['side']} {o['type']} {o['origQty']} @ {o['price']} (Filled: {o['executedQty']})")
    else:
        st.markdown("📭 No recent orders.")

# ------------------------------
# ORDER INPUT FORM
# ------------------------------
st.markdown("---")
st.subheader("📤 Place a New Order")

with st.form("order_form"):
    side = st.selectbox("Side", ["BUY", "SELL"])
    order_type = st.selectbox("Order Type", ["MARKET", "LIMIT", "STOP_MARKET", "STOP_LIMIT"])
    quantity = st.number_input("Quantity", min_value=0.0001, step=0.0001, format="%.4f")

    price = stop_price = None
    if order_type in ["LIMIT", "STOP_LIMIT"]:
        price = st.number_input("Limit Price", min_value=0.0, step=1.0)
    if order_type in ["STOP_MARKET", "STOP_LIMIT"]:
        stop_price = st.number_input("Stop Price", min_value=0.0, step=1.0)

    submitted = st.form_submit_button("📬 Submit Order")

    if submitted:
        result = bot.place_order(symbol, side, order_type, quantity, price, stop_price)
        if result:
            st.success("✅ Order Placed Successfully!")
            st.json(result)
        else:
            st.error("❌ Order failed. Check your inputs or try again.")
