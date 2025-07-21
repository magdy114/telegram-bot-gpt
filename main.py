import os
from openai import OpenAI
from gtts import gTTS
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# إعداد عميل OpenAI
client = OpenAI()

# وضع الصوت (مفعّل)
VOICE_MODE = True

# دالة معالجة الرسائل
def handle_message(update: Update, context: CallbackContext):
    user_input = update.message.text
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        reply = response.choices[0].message.content
        update.message.reply_text(reply)

        # توليد صوت إذا كان مفعلاً
        if VOICE_MODE:
            tts = gTTS(reply, lang='ar')
            audio_file = "response.mp3"
            tts.save(audio_file)

            with open(audio_file, 'rb') as f:
                update.message.reply_voice(f)

    except Exception as e:
        update.message.reply_text(f"حدث خطأ: {e}")

# دالة بدء البوت
def start(update: Update, context: CallbackContext):
    update.message.reply_text("مرحباً بك! أرسل أي سؤال أو اكتب /خطة_الشرح لرؤية خطة الدروس.")

# دالة إرسال خطة الشرح
def send_plan(update: Update, context: CallbackContext):
    update.message.reply_text("📘 خطة الشرح:\n1. النهايات\n2. الاتصال\n3. المشتقات\n...")

def main():
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # تأكد أنك قمت بإضافة المتغير في Railway
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("خطة_الشرح", send_plan))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
