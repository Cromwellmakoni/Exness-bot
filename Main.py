from flask import Flask, jsonify
import threading
import time
import os

app = Flask(name)

@app.route('/')
def home():
return "ExnessBot is Running"

@app.route('/api/healthz')
def healthz():
return jsonify({"status": "ok"})

def run_bot():
# THIS IS WHERE YOUR EXNESS + TELEGRAM LOGIC GOES
# Paste the rest of your bot code from Replit below this line
# Example loop:
while True:
print("Bot checking for Exness alerts...")
time.sleep(60) # checks every 60 seconds

if name == "main":
threading.Thread(target=run_bot, daemon=True).start()
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)