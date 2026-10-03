import websocket, json, threading, time, requests
from flask import Flask

TOKEN = "8782432244:AAFVJ-6YbM6OUpY_7mABBmpi0SobEG1f_po"
CHAT_ID = "6601590106"

app = Flask(__name__)
@app.route('/')
def home(): return "BC Original WS Live - Running"

def send(m):
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
        data={"chat_id": CHAT_ID, "text": m, "parse_mode": "Markdown"}, timeout=5)
    except: pass

last_price = 0
start_price = 0
round_start = time.time()

def on_message(ws, message):
    global last_price, start_price, round_start
    try:
        d = json.loads(message)
        curr = float(d['p']) # trade price

        # 15 sec por por new round
        if time.time() - round_start >= 15:
            round_start = time.time()
            start_price = curr
            send(f"🆕 *NEW ROUND*\n`{curr:.2f}`")

        if last_price != 0:
            diff = curr - last_price
            if abs(diff) >= 0.25: # 0.25$ নড়লেই signal
                icon = "🟢 UP" if diff > 0 else "🔴 DOWN"
                sec = int(time.time() - round_start)
                trend = "UP" if curr > start_price else "DOWN"
                send(f"{icon} `{last_price:.2f}` -> `{curr:.2f}`\n⏱ {sec}/15s | Trend: {trend}")

        last_price = curr
    except: pass

def on_open(ws):
    send("✅ *WS Connected - 0 Delay Live*")

def run_ws():
    while True:
        try:
           
