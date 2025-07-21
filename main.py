import openai
from gtts import gTTS
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

import os

# دالة الرد على الرسائل
def handle_message(update: Update, context: CallbackContext):
    user_input = update.message.text
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        reply = response['choices'][0]['message']['content']
        update.message.reply_text(reply)

        # إرسال الرد صوتيًا إذا كانت الصوت مفعّلة
        if VOICE_MODE:
            tts = gTTS(reply, lang='ar')
            audio_file = "response.mp3"
            tts.save(audio_file)
            with open(audio_file, 'rb') as f:
                update.message.reply_voice(f)

    except Exception as e:
        update.message.reply_text(f"حدث خطأ: {e}")

# أوامر البوت
def start(update: Update, context: CallbackContext):
    update.message.reply_text("أهلًا بك! أرسل أي سؤال أو اكتب /خطة_الشرح لرؤية خطة الشرح.")

def limits(update: Update, context: CallbackContext):
    update.message.reply_text("الحد الأقصى للاستخدام اليومي هو 100 رسالة.")

def send_plan(update: Update, context: CallbackContext):
    update.message.reply_text("هذه هي خطة الشرح: \n1. النهايات\n2. الاتصال\n3. المشتقات")

# التشغيل الرئيسي
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("limits", limits))
dp.add_handler(CommandHandler("plan", send_plan))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    # قراءة المتغيرات من بيئة ريلواي
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    VOICE_MODE = os.environ.get("VOICE_MODE") == "1"

    openai.api_key = OPENAI_API_KEY

    main()
