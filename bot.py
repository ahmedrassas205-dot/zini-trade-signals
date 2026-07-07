from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

from config import TOKEN, ADMIN_ID, USERS_FILE
from signal_manager import create_signal, build_message


def save_user(chat_id):
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w"):
            pass

    with open(USERS_FILE, "r") as file:
        users = file.read().splitlines()

    if str(chat_id) not in users:
        with open(USERS_FILE, "a") as file:
            file.write(f"{chat_id}\n")


def get_users():
    if not os.path.exists(USERS_FILE):
        return []

    with open(USERS_FILE, "r") as file:
        return file.read().splitlines()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    save_user(chat_id)

    await update.message.reply_text(
        "👋 أهلاً بك في Zini Trade Signals\n\n"
        "✅ تم تسجيل اشتراكك بنجاح.\n"
        "قريبًا ستصلك إشارات الذهب مباشرة."
    )


async def users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    count = len(get_users())
    await update.message.reply_text(f"📊 عدد المشتركين: {count}")


async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"🆔 Your Chat ID:\n{update.effective_chat.id}"
    )


async def send(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_chat.id != ADMIN_ID:
        await update.message.reply_text("❌ ليس لديك صلاحية.")
        return

    if len(context.args) != 6:
        await update.message.reply_text(
            "الاستخدام الصحيح:\n"
            "/send BUY 3345.20 3338.00 3350.00 3355.00 3362.00"
        )
        return

    signal_type = context.args[0]
    entry = context.args[1]
    sl = context.args[2]
    tp1 = context.args[3]
    tp2 = context.args[4]
    tp3 = context.args[5]

    signal = create_signal(
        signal_type,
        entry,
        sl,
        tp1,
        tp2,
        tp3
    )

    message = build_message(signal)

    sent = 0

    for user in get_users():
        try:
            await context.bot.send_message(
                chat_id=int(user),
                text=message
            )
            sent += 1
        except Exception:
            pass

    await update.message.reply_text(
        f"✅ تم إرسال الإشارة رقم #{signal['id']:04d}\n"
        f"📤 تم الإرسال إلى {sent} مشترك."
    )


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("users", users))
app.add_handler(CommandHandler("id", myid))
app.add_handler(CommandHandler("send", send))

print("✅ Zini Trade Signals Started...")

app.run_polling()