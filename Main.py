from flask import Flask
import os, threading, time, requests

app = Flask(__name__)

# YOUR BOT TOKEN + YOUR CHAT_ID
TELEGRAM_TOKEN = "8841386835:AAHOA3Dmtqm7y8hW1QfLc4fUi5IqyqVtuAw"
CHAT_ID = 7626173408 # <-- YOUR ID

SYMBOL = "EURUSD"
CHECK_INTERVAL = 300 # 5 minutes

def send_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = {"chat_id": CHAT_ID, "text": msg}
        requests.post(url, data=data, timeout=10)
    except Exception as e:
        print("Telegram error:", e)

def get_price(symbol):
    try:
        base = symbol[:3]
        quote = symbol[3:]
        url = f"https://api.exchangerate-api.com/v4/latest/{base}"
        r = requests.get(url, timeout=10).json()
        rate = r["rates"][quote]
        return rate
    except:
        return None

def price_checker():
    last_price = None
    send_telegram("✅ ExnessBot Started! Checking prices every 5 min")
    
    while True:
        price = get_price(SYMBOL)
        if price:
            msg = f"📊 {SYMBOL}: {price:.5f}"
            if last_price and abs(price - last_price) > 0.0010:
                send_telegram(f"🚨 BIG MOVE! {SYMBOL}\nOld: {last_price:.5f}\nNew: {price:.5f}")
            last_price = price
            print(msg)
        time.sleep(CHECK_INTERVAL)

@app.route('/')
def home():
    return "ExnessBot is Running and Checking Prices"

if __name__ == "__main__":
    threading.Thread(target=price_checker, daemon=True).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
