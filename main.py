import os
import openai
from gtts import gTTS
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# إعداد مفتاح OpenAI من متغير البيئة
openai.api_key = os.getenv("OPENAI_API_KEY")

# تفعيل الصوت
VOICE_MODE = True

def handle_message(update: Update, context: CallbackContext):
    user_input = update.message.text
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        reply = response.choices[0].message["content"]
        update.message.reply_text(reply)

        if VOICE_MODE:
            tts = gTTS(reply, lang='ar')
            tts.save("response.mp3")
            with open("response.mp3", 'rb') as f:
                update.message.reply_voice(f)

    except Exception as e:
        update.message.reply_text(f"❌ حدث خطأ: {e}")

def start(update: Update, context: CallbackContext):
    update.message.reply_text("أهلًا بك في مساعد مجدي للرياضيات. أرسل سؤالك أو اكتب /خطة_الشرح لرؤية الدروس.")

def send_plan(update: Update, context: CallbackContext):
    update.message.reply_text("📘 خطة الشرح:\n1. النهايات\n2. الاتصال\n3. المشتقات\n...")

def main():
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    if not TOKEN:
        raise ValueError("❌ خطأ: لم يتم تعيين متغير TELEGRAM_BOT_TOKEN في البيئة")

    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("خطة_الشرح", send_plan))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
