import threading, time, requests
from flask import Flask
from collections import deque

TOKEN = "8782432244:AAFVJ-6YbM6OUpY_7mABBmpi0SobEG1f_po"
CHAT_ID = "6601590106"

app = Flask(__name__)

@app.route('/')
def home():
    return "15 Sec BC Bot Live"

def send(m):
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": m}, timeout=10)
    except: pass

def price_loop():
    send("✅ 15 Sec Bot Chalu - 10s Bet + 5s Play")
    prices = deque(maxlen=10)
    while True:
        try:
            sec = int(time.time()) % 15
            res = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=5)
            curr = float(res.json()['price'])
            prices.append(curr)
            print(f"Sec: {sec} | Price: {curr}")
            if sec == 10 and len(prices) >= 5:
                first = prices[0]
                last = prices[-1]
                diff = last - first
                if diff > 0.3:
                    send(f"🟢 UP Signal | {first:.2f} -> {last:.2f}\nBet dhorar time ekhon! 4 sec baki")
                elif diff < -0.3:
                    send(f"🔴 DOWN Signal | {first:.2f} -> {last:.2f}\nBet dhorar time ekhon! 4 sec baki")
                else:
                    send(f"⚪ SIDEWAYS | {last:.2f} - Skip koro")
                prices.clear()
                time.sleep(6)
            time.sleep(1)
        except Exception as e:
            print(e)
            time.sleep(1)

threading.Thread(target=price_loop, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
