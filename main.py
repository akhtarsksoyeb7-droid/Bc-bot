from flask import Flask
from threading import Thread
import os, time, requests

app = Flask('')
@app.route('/')
def home(): return "BC.Game 5s Bot Live"

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

OFFSET = -70.0 # তোমার জন্য -70 করে দিলাম, এতে BC.Game এর সাথে মিলে যাবে

def send_telegram(text):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": text}, timeout=10)
    except: pass

def get_price():
    headers = {"User-Agent": "Mozilla/5.0"}
    sources = [
        ("bybit", "https://api.bybit.com/v5/market/tickers?category=spot&symbol=BTCUSDT", lambda j: float(j['result']['list'][0]['lastPrice'])),
        ("okx", "https://www.okx.com/api/v5/market/ticker?instId=BTC-USDT", lambda j: float(j['data'][0]['last'])),
        ("binance", "https://data-api.binance.vision/api/v3/ticker/price?symbol=BTCUSDT", lambda j: float(j['price'])),
    ]
    for name, url, parser in sources:
        try:
            r = requests.get(url, timeout=5, headers=headers)
            if r.status_code == 200:
                return parser(r.json()) + OFFSET
        except: pass
    return None

def bot_loop():
    send_telegram("BC.Game Bot ON ✅\nOffset -70 applied, now price will match")
    while True:
        try:
            start_price = get_price()
            if not start_price:
                time.sleep(2)
                continue
            time.sleep(5)
            end_price = get_price()
            if not end_price: end_price = start_price
            diff = end_price - start_price

            if diff > 0:
                msg = f"🟢 UP ⬆️\n{start_price:.2f} -> {end_price:.2f}"
            elif diff < 0:
                msg = f"🔴 DOWN ⬇️\n{start_price:.2f} -> {end_price:.2f}"
            else:
                msg = f"⚪ SAME {start_price:.2f}"

            print(msg)
            send_telegram(msg)
        except Exception as e:
            print(e)
            time.sleep(2)

Thread(target=bot_loop, daemon=True).start()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
