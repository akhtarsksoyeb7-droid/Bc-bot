import os
import random
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Token Render er Environment Variable theke asbe - Git e token dibi na
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Demo Balance - Real taka na
user_balance = {}

# Demo Crash Logic - Asol Aviator er moto 80% dekhte same, kintu server logic na
def get_crash_point():
    # 90% somoy 1.1x - 5x er moddhe crash, 10% somoy boro
    r = random.random()
    if r < 0.9:
        return round(random.uniform(1.1, 5.0), 2)
    else:
        return round(random.uniform(5.0, 50.0), 2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_balance:
        user_balance[user_id] = 1000  # Demo coin
    
    keyboard = [
        [InlineKeyboardButton("✈️ Demo Aviator Khelo", callback_data="play")],
        [InlineKeyboardButton("💰 Balance Dekho", callback_data="balance")],
        [InlineKeyboardButton("ℹ️ Info", callback_data="info")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"Welcome Sidi Jojo Bhai! 👋\n\n"
        f"Eta Aviator er DEMO bot. Kono real taka na.\n"
        f"Tomar Demo Balance: {user_balance[user_id]} coin\n\n"
        f"Niche Menu theke select koro:",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    
    if query.data == "balance":
        bal = user_balance.get(user_id, 1000)
        await query.edit_message_text(f"Tomar Demo Balance: {bal} coin (Real taka na)")

    elif query.data == "info":
        await query.edit_message_text(
            "Eta ekta Educational Demo Bot.\n"
            "Real Aviator er crash server side e hoy, eta keu hack korte pare na.\n"
            "Eta sudhu dekhte kemon lage seta sekhar jonno.\n"
            "18+ Only | No Real Money Involved"
        )

    elif query.data == "play":
        crash_point = get_crash_point()
        msg = await query.edit_message_text(f"✈️ Plane urche... 1.00x")
        
        multiplier = 1.0
        while multiplier < crash_point:
            multiplier += 0.15
            multiplier = round(multiplier, 2)
            try:
                await msg.edit_text(f"✈️ Plane urche... {multiplier}x\n\nCashout korte /cashout likho")
            except:
                pass
            await asyncio.sleep(0.3)
        
        await msg.edit_text(f"💥 CRASHED at {crash_point}x!\n\nAbar khelte /start dao.")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Bot Running...")
    app.run_polling()

if __name__ == "__main__":
    main()
