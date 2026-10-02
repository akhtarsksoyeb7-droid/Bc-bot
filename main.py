import requests, time, json, websocket, threading, os
from flask import Flask

TELEGRAM_TOKEN = "8782432244:AAF4mlrFhI62DqoFv_4QityqX_J5uqIH0hA"
CHAT_ID = "6601590106"
live_price = 0

app = Flask(__name__)
@app.route('/')
def home():
    return "BC Bot Live"

def tg_send(text):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": text}, timeout=5)
    except: pass

def on_message(ws, message):
    global live_price
    try:
        data = json.loads(message)
        live_price = float(data['p'])
    except: pass

def send_every_5_sec():
    while True:
        time.sleep(5)
        if live_price == 0: continue
        
        open_price = live_price
        time.sleep(5) # 5 sec candle wait
        close_price = live_price
        
        if close_price == 0: continue
        
        diff = close_price - open_price
        diff_percent = (diff / open_price) * 100
        now = time.strftime('%H:%M:%S')
        
        if diff > 0:
            msg = f"🟢 5s CANDLE UP - {now}\n\n🔓 Open: {open_price:.2f}\n🔒 Close: {close_price:.2f}\n📈 Change: +{diff:.2f} (+{diff_percent:.3f}%)\n\n👉 BC Game e UP maro!"
        elif diff < 0:
            msg = f"🔴 5s CANDLE DOWN - {now}\n\n🔓 Open: {open_price:.2f}\n🔒 Close: {close_price:.2f}\n📉 Change: {diff:.2f} ({diff_percent:.3f}%)\n\n👉 BC Game e DOWN maro!"
        else:
            msg = f"⚪ 5s SAME - {now}\nPrice: {close_price:.2f}"
        
        print(msg)
        tg_send(msg)

def start_ws():
    while True:
        try:
            ws = websocket.WebSocketApp("wss://stream.binance.com:9443/ws/btcusdt@trade", on_message=on_message)
            ws.run_forever()
        except: time.sleep(5)

tg_send("✅ Bot Update Done Bhai\nEbar Open/Close Rate sob dekhabe!")

threading.Thread(target=send_every_5_sec, daemon=True).start()
threading.Thread(target=start_ws, daemon=True).start()

port = int(os.environ.get("PORT", 10000))
app.run(host='0.0.0.0', port=port)
