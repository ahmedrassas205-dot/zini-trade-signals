import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("8813168774:AAGptYZfQkr0_OwJkslYx_4tYTEhUR05rrg")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 أهلاً بك في Zini Trade Signals\n\n"
        "البوت يعمل بنجاح.\n"
        "قريباً سيبدأ بإرسال إشارات الذهب."
    )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.run_polling()
