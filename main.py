import time, requests, os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def get_price():
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=5)
        return float(r.json()['price'])
    except:
        return None

def send(t):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": t})

p = get_price()
send("30s Bot Started")

while True:
    time.sleep(25)
    c = get_price()
    if not c or not p:
        continue
    d = c - p
    if d > 2:
        send(f"UP {d:.2f}")
    elif d < -2:
        send(f"DOWN {d:.2f}")
    else:
        send(f"SKIP {d:.2f}")
    p = c
