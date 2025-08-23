#!/usr/bin/env python3

import os
import json
import time
import threading
import google.generativeai as genai
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# --- Gemini ---
genai.configure(api_key=os.getenv("GEMINI_API_KEY", "your-api-key"))
MODEL = "gemini-1.5-flash" # or "gemini-1.5-pro"

ADMIN = os.getenv("ADMIN", "@GustyxPower") # your username
TOKEN = os.getenv("GEMINI_TOKEN", "your-bot-token")
DATA_FILE = "users.json"

# --- persist user data ---
lock = threading.Lock()

def load():
    with lock:
        try:
            return json.load(open(DATA_FILE))
        except FileNotFoundError:
            return {}

def save(data):
    with lock:
        json.dump(data, open(DATA_FILE, "w"), indent=2)

def can_use(uid, name):
    data = load()
    now = time.time()

    if str(uid) not in data:
        data[str(uid)] = {"count": 0, "reset": now + 1800, "premium": False}
    u = data[str(uid)]

    if now > u["reset"]:
        u["count"] = 0
        u["reset"] = now + 1800

    if name == ADMIN:
        u["premium"] = True

    if u["premium"]:
        save(data)
        return True, u["count"]

    if u["count"] >= 30: # you can change limit this
        save(data)
        return False, 30

    u["count"] += 1
    save(data)
    return True, u["count"]

def ask_gemini(prompt):
    try:
        model = genai.GenerativeModel(MODEL)
        r = model.generate_content(prompt, generation_config={"max_output_tokens": 150}) # You can change this
        return r.text.strip()
    except Exception as e:
        return f"🤖 Gemini error: {e}"

# --- command /start ---
# Example Code
# You Can Change This Message
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hi! I'm a Gemini-1.5 backup bot.\n"
        "📌 General user: max 30 prompts / 30 minutes.\n"
        "💰 Premium: IDR 15,000 for unlimited access, type /premium.\n"
        "🎯 In groups: tag @bot or reply to my message."
    )

# --- command /help ---
# Example Code
# You Can Change This Message
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 How to use:\n"
        "• In group: tag @bot or reply to my message.\n"
        "• In private: type your question directly.\n"
        "• Limit 30 prompts / 30 minutes. Type /premium for unlimited."
    )

# --- command /premium ---
# Example Code
# You Can Change This Message
async def premium_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💰 Send IDR 15,000 to <number> then DM @yourusername with proof."
    )

# --- handler pesan (mention / reply only) ---
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    bot_username = (await context.bot.get_me()).username
    text = update.message.text
    mention = f"@{bot_username}" if bot_username else ""
    is_mentioned = mention and mention in text
    is_reply = update.message.reply_to_message and update.message.reply_to_message.from_user.id == context.bot.id

    if not (is_mentioned or is_reply):
        return

    user = update.effective_user
    ok, used = can_use(user.id, user.username or user.first_name)
    if not ok:
        await update.message.reply_text(
            "⚠️ Limit of 30 prompts / 30 minutes reached.\nType /premium to upgrade." # Example Comments
        )
        return

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action="typing"
    )

    prompt = text.replace(mention, "").strip()
    reply = ask_gemini(prompt)
    await update.message.reply_text(reply)

# --- main ---
if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("premium", premium_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    print("Bot Gemini ready! Enjoy.")
    app.run_polling()