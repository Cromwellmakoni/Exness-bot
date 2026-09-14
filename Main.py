from flask import Flask
import os, threading, time, requests

app = Flask(__name__)

TELEGRAM_TOKEN = "8841386835:AAHOA3Dmtqm7y8hW1QfLc4fUi5IqyqVtuAw"
CHAT_ID = None # will fill automatically

SYMBOL = "EURUSD"
CHECK_INTERVAL = 300

def send_telegram(msg):
    global CHAT_ID
    if not CHAT_ID: # get chat_id from last message
        try:
            r = requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates").json()
            if r["result"]:
                CHAT_ID = r["result"][-1]["message"]["chat"]["id"]
        except: pass
    
    if CHAT_ID:
        try:
            requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", 
                          data={"chat_id": CHAT_ID, "text": msg})
        except Exception as e: print(e)

def get_price(symbol):
    try:
        base = symbol[:3]
        quote = symbol[3:]
        url = f"https://api.exchangerate-api.com/v4/latest/{base}"
        r = requests.get(url, timeout=10).json()
        return r["rates"][quote]
    except: return None

def price_checker():
    last_price = None
    time.sleep(10) # wait 10s for bot to start
    send_telegram("✅ ExnessBot Started! Checking prices every 5 min")
    
    while True:
        price = get_price(SYMBOL)
        if price:
            if last_price and abs(price - last_price) > 0.0010:
                send_telegram(f"🚨 BIG MOVE! {SYMBOL}\nOld: {last_price:.5f}\nNew: {price:.5f}")
            last_price = price
            print(f"📊 {SYMBOL}: {price:.5f}")
        time.sleep(CHECK_INTERVAL)

@app.route('/')
def home():
    return "ExnessBot is Running"

if __name__ == "__main__":
    threading.Thread(target=price_checker, daemon=True).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
