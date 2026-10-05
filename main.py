import threading, time, requests
from flask import Flask
from collections import deque
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = "6601590106"

app = Flask(__name__)

@app.route('/')
def home():
    return "Final Bot Live - Jojo Board Active"

def send(m):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        r = requests.post(url, data={"chat_id": CHAT_ID, "text": m}, timeout=10)
        print(f"SENT: {m} | {r.status_code}")
    except Exception as e:
        print(f"SEND FAIL: {e}")

def price_loop():
    prices = deque(maxlen=10)
    last_slot = -1
    print("Price Loop Started...")
    while True:
        try:
            # Eta India teo kaj korbe
            url = "https://data-api.binance.vision/api/v3/ticker/price?symbol=BTCUSDT"
            curr = float(requests.get(url, timeout=5).json()['price'])
            prices.append(curr)

            sec = int(time.time()) % 15
            slot = int(time.time() / 15)
            print(f"Sec {sec} Price {curr}")

            if sec == 10 and slot!= last_slot:
                diff = curr - prices[0] if len(prices) > 0 else 0
                if diff > 0.5:
                    send(f"🟢 UP {prices[0]:.2f} -> {curr:.2f} Diff {diff:.2f}")
                elif diff < -0.5:
                    send(f"🔴 DOWN {prices[0]:.2f} -> {curr:.2f} Diff {diff:.2f}")
                else:
                    send(f"⚪ SKIP {curr:.2f} Diff {diff:.2f}")

                last_slot = slot
                prices.clear()
                time.sleep(6)
            time.sleep(1)
        except Exception as e:
            print(f"LOOP ERROR: {e}")
            time.sleep(2)

print("Bot Started with vision API")
threading.Thread(target=price_loop, daemon=True).start()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
