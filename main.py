import time
import requests
from flask import Flask
import threading

# --- SETTING ---
TELEGRAM_TOKEN = "8782432244:AAFVJ-6YbM6OUpY_7mABBmpi0SobEG1f_po"
CHAT_ID = "6601590106"

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Live! 5s Signal Running..."

def send_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
        requests.post(url, data=data, timeout=10)
    except Exception as e:
        print(f"Telegram Error: {e}")

def trading_loop():
    send_telegram("✅ *Bot Update Done Bhai*\nEbar Open/Close Rate sob dekhabe!\n5s Signal Start Holo!")
    last_price = 0
    while True:
        try:
            # Binance theke BTC price nebe
            res = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=10).json()
            current_price = float(res['price'])
            
            if last_price != 0:
                if current_price > last_price:
                    diff = current_price - last_price
                    msg = f"🟢 *5s CANDLE UP - {time.strftime('%H:%M:%S')}*\n🔓 Open: `{last_price:.2f}`\n🔒 Close: `{current_price:.2f}`\n📈 Change: `+{diff:.2f}`\n👉 BC Game e *UP* maro!"
                    send_telegram(msg)
                elif current_price < last_price:
                    diff = last_price - current_price
                    msg = f"🔴 *5s CANDLE DOWN - {time.strftime('%H:%M:%S')}*\n🔓 Open: `{last_price:.2f}`\n🔒 Close: `{current_price:.2f}`\n📉 Change: `-{diff:.2f}`\n👉 BC Game e *DOWN* maro!"
                    send_telegram(msg)
                else:
                    msg = f"⚪ *5s DOJI - {time.strftime('%H:%M:%S')}*\nPrice Same: `{current_price:.2f}`"
                    send_telegram(msg)

            last_price = current_price
            time.sleep(5)

        except Exception as e:
            print(f"Loop Error: {e}")
            time.sleep(5)

# Thread start
threading.Thread(target=trading_loop, daemon=True).start()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
