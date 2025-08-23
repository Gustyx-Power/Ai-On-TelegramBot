#!/usr/bin/env python3

import os
import json
import time
import threading
import requests
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:1b"
ADMIN = os.getenv("ADMIN", "@GustyxPower") # Replace with your Telegram Username
TOKEN = os.getenv("TOKEN") # Replace with your Telegram Bot Token
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

    if u["count"] >= 50:
        save(data)
        return False, 50

    u["count"] += 1
    save(data)
    return True, u["count"]

def ask_ollama(prompt):
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "options": {
            "num_gpu": 99,  
            "main_gpu": 0,     
            "num_thread": 4     
        },
        "stream": False
    }
    try:
        r = requests.post(OLLAMA_URL, json=payload, timeout=240)
        return r.json().get("response", "🤖 Maaf, aku lagi error.")
    except Exception as e:
        return f"🤖 Error: {e}"

# --- command /start  ---
# Example Code
# You Can Change This Message
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hi! I am a local AI bot based on *Ollama*.\n" # Example If You Use Ollama
        "📌 General users: max 50 prompts / 30 minutes.\n" # Example If You Change Limit Information
        "💰 Premium: IDR 10,000 for unlimited access, type /premium." # Example If user Change Premium Information
    )

# --- command /premium ---
# Example Code
# You Can Change This Message
async def premium_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💰 Send IDR 10,000 to <number> then DM @GustyxPower with proof." # For Example If You Add Premium Feature
    )

# --- handler ---
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    user = update.effective_user
    ok, used = can_use(user.id, user.username or user.first_name)

    if not ok:
        await update.message.reply_text(
            f"⚠️ Limit of 150 prompts / 30 minutes reached.\nType /premium to upgrade." # Example If You Change Limit Information
        )
        return

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action="typing"
    )

    prompt = update.message.text
    reply = ask_ollama(prompt)
    await update.message.reply_text(reply)

# --- main ---
if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("premium", premium_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    print("Bot Telegram + Ollama (GPU-offload) ready. Enjoy!")
    app.run_polling()