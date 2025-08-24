#!/usr/bin/env python3

import os
import re
import html
import json
import time
import threading
import openai
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# --- konfigurasi OpenAI-compat Groq ---
openai.api_key = os.getenv("GROQ_API_KEY", "your-api_key")
openai.base_url = "https://api.groq.com/openai/v1/"
# --- Add your model here (Remove # on MODEL if you use)---
# MODEL = "llama-3.3-70b-versatile"
# MODEL = "moonshotai/kimi-k2-instruct"

ADMIN = os.getenv("ADMIN", "@GustyxPower")
TOKEN = os.getenv("TOKEN")
DATA_FILE = "users.json"
GROUPS_FILE = "groups.json"

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

def load_groups():
    with lock:
        try:
            return json.load(open(GROUPS_FILE))
        except FileNotFoundError:
            return {}

def save_groups(groups):
    with lock:
        json.dump(groups, open(GROUPS_FILE, "w"), indent=2)

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

    if u["count"] >= 30:
        save(data)
        return False, 30

    u["count"] += 1
    save(data)
    return True, u["count"]

# --- helper split long message ---
def escape_html(text: str) -> str:
    """HTML escape special characters."""
    return html.escape(text)
    
def split_message(text: str, chunk_size: int = 4000):
    """Splits a message if it's too long because Telegram has a 4096 character limit."""
    return [text[i:i+chunk_size] for i in
        range(0, len(text), chunk_size)]


# --- language detection + AI function ---
def detect_language(text: str) -> str:
    """Deteksi bahasa berdasarkan isi teks."""
    text_lower = text.lower()
    if "fun main" in text_lower or "val " in text_lower:
        return "kotlin"
    if "public static void main" in text_lower or "class " in text_lower:
        return "java"
    if "package main" in text_lower or "fmt." in text_lower:
        return "go"
    if "fn main" in text_lower or "let mut" in text_lower:
        return "rust"
    if text_lower.startswith("#!") or text_lower.startswith("$ ") or "echo " in text_lower:
        return "shell"
    if "def " in text_lower and ":" in text_lower:
        return "python"
    if "<html" in text_lower or "<div" in text_lower:
        return "html"
    if "function " in text_lower or "console.log" in text_lower:
        return "javascript"
    return "txt"


def ask_groq(prompt: str) -> str:
    try:
        r = openai.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800,
            temperature=0.3,
            top_p=0.8
        )
        reply = r.choices[0].message.content.strip()

        # Kalau AI sudah kasih blok kode sendiri, langsung kembalikan (escape dulu)
        if "```" in reply:
            return f"<pre><code>{escape_html(reply)}</code></pre>"

        # Deteksi bahasa otomatis
        lang = detect_language(reply)

        # Bungkus ke dalam HTML code block
        reply = f"<pre><code class=\"language-{lang}\">{escape_html(reply)}</code></pre>"

        return reply

    except Exception as e:
        return f"🤖 Chatbot error: {escape_html(str(e))}"


        
# --- command /start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hai! Aku bot XMS AI berbasis Groq + LLM 3.3 + KIMI K2 + OpenAi.\n"
        "📌 User umum: max 30 prompt / 30 menit.\n"
        "💰 Premium: Rp 15.000 unlimited, ketik /premium.\n"
        "🎯 Di grup: tag @bot atau reply pesanku."
    )

# --- command /help ---
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 Cara pakai:\n"
        "• Di grup: tag @gustyxai_bot atau reply pesanku.\n"
        "• Di private: langsung ketik pertanyaan.\n"
        "• Limit 30 prompt / 30 menit. Ketik /premium untuk unlimited."
    )

# --- command /premium ---
async def premium_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💰 Kirim Rp 15.000 ke DM @GustyxPower dengan bukti."
    )

# --- command /reload ---
async def reload_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("last_prompt"):
        await update.message.reply_text("Tidak ada prompt sebelumnya untuk diulang.")
        return
    prompt = context.user_data["last_prompt"]
    await update.message.reply_text("🔄 Mengulang prompt...")
    reply = ask_groq(prompt)
    await update.message.reply_text(reply,parse_mode="Markdown")

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
            "⚠️ Limit 30 prompt / 30 menit habis.\nKetik /premium untuk upgrade."
        )
        return

    chat = update.effective_chat
    if chat.type in (chat.GROUP, chat.SUPERGROUP):
        groups = load_groups()
        groups[str(chat.id)] = chat.title
        save_groups(groups)

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action="typing"
    )
    await update.message.reply_text("🤖 Sedang berpikir...")

    prompt = text.replace(mention, "").strip()
    context.user_data["last_prompt"] = prompt
    reply = ask_groq(prompt)

    # Split kalau terlalu panjang
    for part in split_message(reply):
        await update.message.reply_text(part, parse_mode="HTML")

    await update.message.reply_text("🤖 Selesai menjawab.")

# --- main ---
if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("premium", premium_cmd))
    app.add_handler(CommandHandler("reload", reload_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    print("Bot Groq ready! Enjoy.")
    app.run_polling()