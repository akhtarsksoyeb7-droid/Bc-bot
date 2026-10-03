import websocket, json, threading, time, requests
from flask import Flask

TOKEN = "8782432244:AAFVJ-6YbM6OUpY_7mABBmpi0SobEG1f_po"
CHAT_ID = "6601590106"

app = Flask(__name__)

@app.route('/')
def home():
    return "Running"

def send(m):
    try:
        r = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": m}, timeout=10)
        print(f"Telegram reply: {r.text}")
    except Exception as e:
        print(f"Send error: {e}")

last_price = 0
def on_message(ws, message):
    global last_price
    try:
        data = json.loads(message)
        if 'p' in data:
            curr = float(data['p'])
            # Ekhane 0.01 kore dilam, tahole prottek choto move e message asbe
            if last_price != 0 and abs(curr - last_price) >= 0.01:
                icon = "🟢 UP" if curr > last_price else "🔴 DOWN"
                send(f"{icon} {last_price:.2f} -> {curr:.2f}")
            last_price = curr
            print(curr)
    except Exception as e:
        print(e)

def start_ws():
    send("✅ Bot Chalu Hoiche - Render e Deploy Success")
    while True:
        try:
            ws = websocket.WebSocketApp("wss://stream.binance.com:9443/ws/btcusdt@trade", on_message=on_message)
            ws.run_forever(ping_interval=20)
        except Exception as e:
            print(e)
            time.sleep(2)

threading.Thread(target=start_ws, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
           
