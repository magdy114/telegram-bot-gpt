import os
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import openai

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
VOICE_MODE = os.getenv("VOICE_MODE", "false").lower() == "true"

openai.api_key = OPENAI_API_KEY

def start(update, context):
    update.message.reply_text("مرحباً بك في Magdy Math Assistant! أرسل /limits أو /خطة_الدراسة")

def limits(update, context):
    update.message.reply_text("درس النهايات:\nhttps://youtu.be/kCG2HiM8v0o")

def send_plan(update, context):
    with open("plan_text.txt", "r", encoding="utf-8") as file:
        plan_text = file.read()
    update.message.reply_text(plan_text)

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("limits", limits))
    dp.add_handler(CommandHandler("خطة_الدراسة", send_plan))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
