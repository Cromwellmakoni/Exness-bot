import os
import time
import threading
import requests
from flask import Flask

app = Flask(__name__)

TELEGRAM_TOKEN = "8841386835:AAHOA3Dmtqm7y8hW1QfLc4fUi5IqyqVtuAw"
CHAT_ID = 7626173408

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": message})

def price_checker():
    send_telegram("✅ ExnessBot Started! Testing your CHAT_ID: 7626173408")
    while True:
        try:
            send_telegram("📊 EURUSD: 1.08742 | GBPUSD: 1.27345")
            time.sleep(30)
        except:
            time.sleep(10)

@app.route('/')
def home():
    return "Bot is running!"

if __name__ == "__main__":
    threading.Thread(target=price_checker, daemon=True).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
