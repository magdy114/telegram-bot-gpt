import os
import openai
import telegram
from gtts import gTTS
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
VOICE_MODE = os.getenv("VOICE_MODE", "false").lower() == "true"

openai.api_key = OPENAI_API_KEY

def start(update, context):
    update.message.reply_text("👋 أهلاً بيك! أنا مساعد مجدي للرياضيات. اكتب أي سؤال وهاجاوبك.\n\nلو عايز خطة limits اكتب /limits")

def limits(update, context):
    update.message.reply_text("🔗 خطة limits:\nhttps://youtu.be/kGG2HiM8v0o")

def send_plan(update, context):
    with open("plan_text.txt", "r", encoding="utf-8") as file:
        plan_text = file.read()
    update.message.reply_text(plan_text)

def handle_message(update, context):
    user_input = update.message.text
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        reply = response['choices'][0]['message']['content']

        # إرسال الرد نصًا
        update.message.reply_text(reply)

        # إرسال الرد صوتيًا إذا كانت الميزة مفعلة
        if VOICE_MODE:
            tts = gTTS(reply, lang='ar')
            audio_file = "response.mp3"
            tts.save(audio_file)
            with open(audio_file, 'rb') as f:
                update.message.reply_voice(f)

    except Exception as e:
        update.message.reply_text(f"حدث خطأ: {e}")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("limits", limits))
    dp.add_handler(CommandHandler("خطة_الدراسة", send_plan))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
