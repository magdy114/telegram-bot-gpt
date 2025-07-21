
import os
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import openai

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
VOICE_MODE = os.getenv("VOICE_MODE", "false").lower() == "true"

openai.api_key = OPENAI_API_KEY

def start(update, context):
    update.message.reply_text("مرحبًا بك في Magdy Math Assistant! أرسل /limits أو /خطة للبدء.")

def limits(update, context):
    update.message.reply_text("درس النهايات:
https://youtu.be/kCG2HiM8v0o")

def send_plan(update, context):
    with open("plan_text.txt", "r", encoding="utf-8") as f:
        plan_text = f.read()
    update.message.reply_text(plan_text)
    if VOICE_MODE and os.path.exists("voice.mp3"):
        context.bot.send_voice(chat_id=update.effective_chat.id, voice=open("voice.mp3", "rb"))

def send_file(update, context):
    update.message.reply_document(document=open("lesson_3_limits.pdf", "rb"))
    update.message.reply_document(document=open("lesson_1_tangents.pdf", "rb"))

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("limits", limits))
    dp.add_handler(CommandHandler("خطة", send_plan))
    dp.add_handler(CommandHandler("file", send_file))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
