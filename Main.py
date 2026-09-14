from flask import Flask, jsonify
import threading
import time
import os

app = Flask(__name__)

# Example: your bot running in background
def run_bot():
    while True:
        print("ExnessBot is running...")
        time.sleep(60)

@app.route('/')
def home():
    return "ExnessBot is Running ✅"

@app.route('/api/healthz')
def healthz():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    # Start bot thread
    threading.Thread(target=run_bot, daemon=True).start()
    
    # Render needs this to work
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
