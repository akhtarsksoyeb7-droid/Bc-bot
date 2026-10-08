import os
import time
import requests
from flask import Flask
import threading

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

app = Flask(__name__)

@app.route('/')
def home():
    return "JOJO Bot is Running!"

def send_signal_loop():
    print("Bot Loop Started...")
    while True:
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            message = "🚀 **BC GAME LIVE SIGNAL** 🚀\n\n💰 Game: Crash\n📈 Prediction: Cashout @ 2.10x\n✅ Safe: 1.50x\n\n👉 Join: https://bcgame.com"
            
            data = {
                "chat_id": CHAT_ID,
                "text": message,
                "parse_mode": "Markdown"
            }
            r = requests.post(url, json=data)
            print(f"Sent! Response: {r.text}")
        except Exception as e:
            print(f"Error: {e}")
        
        time.sleep(60) # 60 sec por por jabe

if __name__ == "__main__":
    # Bot ke background e chalao
    t = threading.Thread(target=send_signal_loop)
    t.start()
    # Flask ke samne chalao jate Render bondho na hoy
    app.run(host='0.0.0.0', port=10000)
