import os
import logging
import openai
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

# تفعيل السجل (للتصحيح إن لزم)
logging.basicConfig(level=logging.INFO)

# تحميل التوكينات من المتغيرات البيئية
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# التأكد من وجود التوكينات
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("❌ خطأ: لم يتم تعيين TELEGRAM_BOT_TOKEN في البيئة")

if not OPENAI_API_KEY:
    raise ValueError("❌ خطأ: لم يتم تعيين OPENAI_API_KEY في البيئة")

# تفعيل مفتاح OpenAI
openai.api_key = OPENAI_API_KEY

# أمر: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحباً! أنا مساعدك الذكي في مادة الرياضيات 🎓🧠")

# أمر: /study_plan
async def send_plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📘 هذه خطة الدراسة الخاصة بك: \n1. النهايات\n2. الاتصال\n3. المشتقات\n🔁 تابع التقدم معي خطوة بخطوة!")

# نقطة البداية
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("study_plan", send_plan))

    app.run_polling()

if __name__ == "__main__":
    main()
