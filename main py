from flask import Flask
from threading import Thread
import os, time, requests

app = Flask('')
@app.route('/')
def home(): return "BC.Game 5s Bot Live"

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send_telegram(text):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": text}, timeout=10)
    except Exception as e:
        print(f"TG Error: {e}")

def get_price():
    headers = {"User-Agent": "Mozilla/5.0"}
    sources = [
        ("bybit", "https://api.bybit.com/v5/market/tickers?category=spot&symbol=BTCUSDT", lambda j: float(j['result']['list'][0]['lastPrice'])),
        ("okx", "https://www.okx.com/api/v5/market/ticker?instId=BTC-USDT", lambda j: float(j['data'][0]['last'])),
        ("binance_vision", "https://data-api.binance.vision/api/v3/ticker/price?symbol=BTCUSDT", lambda j: float(j['price'])),
        ("coinbase", "https://api.coinbase.com/v2/prices/BTC-USD/spot", lambda j: float(j['data']['amount'])),
    ]
    for name, url, parser in sources:
        try:
            r = requests.get(url, timeout=5, headers=headers)
            if r.status_code == 200:
                p = parser(r.json())
                print(f"{name}: {p}")
                return p
        except Exception as e:
            print(f"{name} fail")
    return None

def bot_loop():
    send_telegram("BC.Game 5s Bot Started ✅\nBTC/USD tracking ON")
    print("BOT STARTED 5s MODE")

    while True:
        try:
            start_price = get_price()
            if not start_price:
                time.sleep(2)
                continue

            print(f"START: {start_price}")
            time.sleep(5) # BC.Game 5s game

            end_price = get_price()
            if not end_price:
                end_price = start_price

            diff = end_price - start_price

            if diff > 0:
                msg = f"🟢 UP WIN ⬆️\nStart: {start_price:.2f}\nEnd: {end_price:.2f}\n+{diff:.2f}"
            elif diff < 0:
                msg = f"🔴 DOWN WIN ⬇️\nStart: {start_price:.2f}\nEnd: {end_price:.2f}\n{diff:.2f}"
            else:
                msg = f"⚪ SAME\n{start_price:.2f}"

            print(msg)
            send_telegram(msg)

        except Exception as e:
            print(f"Loop error: {e}")
            time.sleep(2)

Thread(target=bot_loop, daemon=True).start()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
