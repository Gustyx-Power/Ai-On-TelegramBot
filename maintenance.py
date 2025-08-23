#!/usr/bin/env python3
"""
Send maintenance message to all groups where the bot is present.
Run once: ./run-mt
"""
import os
import json
import asyncio
from telegram import constants
from telegram.error import Forbidden, RetryAfter
from telegram.ext import Application

TOKEN = os.getenv("TOKEN", "your-bot-token")
MSG = (
    "🛠️ *MAINTENANCE MODE*\n"
    "The bot is undergoing *routine maintenance & performance upgrades*.\n\n"
    "⏰ Estimated return time: **±30 minutes** (could be sooner or later)\n"
    "📌 Features can still be used via DM @GustyxPower if urgent\n"
    "💡 It will be faster & more stable after this!\n\n"
    "We apologize for the inconvenience 🙏"
)
async def main():
    app = Application.builder().token(TOKEN).build()
    await app.initialize()
    async with app:
        try:
            with open("groups.json") as f:
                groups = json.load(f)
        except FileNotFoundError:
            print("No groups saved yet.")
            return
        for gid, title in groups.items():
            try:
                await app.bot.send_message(int(gid), MSG, parse_mode="Markdown")
                print(f"✅ Sent to {title} ({gid})")
            except Exception as e:
                print(f"❌ Failed to send to {gid}: {e}")
if __name__ == "__main__":
    asyncio.run(main())