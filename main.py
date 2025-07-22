import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

BOT_TOKEN = os.environ.get("BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# مقدمة مشجعة باللهجة المصرية
def intro_message():
    return "تمام يا نجم، تعالى نركز كده سوا 💪\n\n"

# رسالة خطة الدرس
PLAN_TEXT = """📘 هذه خطة الدرس:
1. المفاهيم
2. الأمثلة
3. التدريب
4. التقويم
"""

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحبًا! أنا مساعدك الذكي في مادة الرياضيات 🧠")

# أمر /plan
async def send_plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(PLAN_TEXT)

# التعامل مع الرسائل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    pre_prompt = """
أنت مساعد ذكي في مادة الرياضيات للصف الثاني عشر متقدم، تتحدث باللهجة المصرية.
- اعرض النصوص العربية من اليمين لليسار (RTL).
- المعادلات بصيغة LaTeX داخل Block باستخدام $$ ... $$.
- لا تعكس ترتيب المعادلات، وسيب lim على الشمال.
- المعادلة لازم تكون في سطر لوحدها بعد الشرح.
- ابدأ الرد بجملة مشجعة عامية.
- لا تجلب أي ملفات من الإنترنت، بل فقط الملفات اللي أضافها منشئ البوت.
"""

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": pre_prompt},
            {"role": "user", "content": user_message}
        ]
    )

    reply = completion.choices[0].message.content
    await update.message.reply_text(intro_message() + reply, parse_mode="Markdown")

# تشغيل التطبيق
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("plan", send_plan))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()
