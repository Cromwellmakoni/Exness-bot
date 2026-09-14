from flask import Flask
import os, threading, time, requests
from telegram import Bot

app = Flask(__name__)

# YOUR BOT TOKEN
TELEGRAM_TOKEN = "8841386835:AAHOA3Dmtqm7y8hW1QfLc4fUi5IqyqVtuAw"
CHAT_ID = None  # will auto-save when you message the bot first

bot = Bot(token=TELEGRAM_TOKEN)

SYMBOL = "EURUSD"  # change this to what you trade: XAUUSD, GBPUSD, etc
CHECK_INTERVAL = 300  # 300 seconds = 5 minutes

def get_price(symbol):
    """Free price from exchangerate-api. Works for forex. For gold/crypto we’ll change this later"""
    try:
        url = f"https://api.exchangerate-api.com/v4/latest/{symbol[:3]}"
        r = requests.get(url, timeout=10).json()
        rate = r["rates"][symbol[3:]]
        return rate
    except:
        return None

def send_telegram(msg):
    global CHAT_ID
    try:
        # get your chat_id by sending /start to your bot first
        updates = bot.get_updates()
        if updates:
            CHAT_ID = updates[-1].message.chat_id
        if CHAT_ID:
            bot.send_message(chat_id=CHAT_ID, text=msg)
    except Exception as e:
        print("Telegram error:", e)

def price_checker():
    last_price = None
    send_telegram("✅ ExnessBot Started! Checking prices every 5 min")
    
    while True:
        price = get_price(SYMBOL)
        if price:
            msg = f"📊 {SYMBOL}: {price}"
            
            # Alert only if price moved more than 0.0010 = 10 pips
            if last_price and abs(price - last_price) > 0.0010:
                send_telegram(f"🚨 BIG MOVE! {SYMBOL}\nOld: {last_price}\nNew: {price}")
            
            last_price = price
            print(msg)
        
        time.sleep(CHECK_INTERVAL)

@app.route('/')
def home():
    return "ExnessBot is Running and Checking Prices"

if __name__ == "__main__":
    # start price checker in background
    threading.Thread(target=price_checker, daemon=True).start()
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
