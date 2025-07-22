from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

# رسالة الترحيب
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("\U0001F44B مرحباً! أنا مساعدك الذكي في مادة الرياضيات \U0001F9E0\nاكتب /plan لرؤية خطة الدرس أو /test لحل اختبار.")

# إرسال خطة الدرس من ملف نصي
async def send_plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        with open("plan_text.txt", "r", encoding="utf-8") as f:
            content = f.read()
        await update.message.reply_text(content)
    except FileNotFoundError:
        await update.message.reply_text("عذرًا، لم أجد خطة الدرس حتى الآن.")

# إرسال اختبار بسيط
async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = "ما نهاية الدالة التالية: f(x) = (x^2 - 9)/(x - 3) عندما x تقترب من 3؟\n"
    options = ["6", "9", "3", "0"]
    await update.message.reply_poll(
        question=question,
        options=options,
        type='quiz',
        correct_option_id=0
    )

# إعداد التطبيق وربط الأوامر
app = ApplicationBuilder().token("YOUR_BOT_TOKEN").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("plan", send_plan))
app.add_handler(CommandHandler("test", test))

# تشغيل البوت
app.run_polling()
