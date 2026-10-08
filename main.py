import os
import asyncio
from telegram import Bot
from flask import Flask
import threading

# Render theke Token ar Chat ID nibe
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID") # Tomar Group ID: -100xxxxxx

app = Flask(__name__)
bot = Bot(token=BOT_TOKEN)

@app.route('/')
def home():
    return "JOJO Bot is Running!"

async def send_signal():
    while True:
        try:
            # BC GAME er direct dam ekhane asbe
            message = "🚀 BC GAME LIVE SIGNAL 🚀\n\n💰 Game: Crash\n📈 Prediction: Cashout @ 2.10x\n✅ Safe Mode: 1.50x\n\n👉 Link: https://bcgame.com"
            await bot.send_message(chat_id=CHAT_ID, text=message)
            print("Signal Sent")
        except Exception as e:
            print(e)
        await asyncio.sleep(60) # 60 second por por signal jabe

def run_flask():
    app.run(host='0.0.0.0', port=10000)

if __name__ == "__main__":
    # Flask ke alada thread e chalabe jate Render ON thake
    threading.Thread(target=run_flask).start()
    asyncio.run(send_signal())
