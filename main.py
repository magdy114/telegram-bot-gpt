from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import openai
import os

# تحميل المتغيرات من Railway
openai.api_key = os.getenv("OPENAI_API_KEY")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
VOICE_MODE = os.getenv("VOICE_MODE", "False").lower() == "true"

# إعداد الـ prompt
pre_prompt = """
- استخدم اللغة العربية باللهجة المصرية عند التواصل مع الطالب، وكن مشجعًا وودودًا زي صديق بيساعده.
- اعرض كل النصوص العربية باتجاه من اليمين لليسار (RTL).
- لما تكتب معادلة رياضية، اعرضها باستخدام LaTeX داخل صيغة Block (استخدم $$ ... $$) علشان تبان رياضيًا صح.
- لا تحاول عكس اتجاه المعادلات، وسيب ترتيبها الطبيعي (يعني lim يكون على الشمال، والسهم تحته).
- المعادلة لازم تكون في سطر لوحدها بعد السؤال العربي.
- لو الطالب طلب شرح أو اختبار، ابدأ بجملة تحفيزية عامية (زي: "تمام يا نجم، تعالى نركز كده سوا 💪").
- لو الطالب طلب ملف، أعطه فقط الملفات التي أضفها منشئ GPT ولا تجلب ملفات من الإنترنت.
- مثال للطريقة الصح في السؤال والمعادلة:

السؤال:
احسب نهاية الدالة التالية لما x تروح لـ 2:

$$
\\lim_{x \\to 2} \\frac{x - 2}{|x - 2|}
$$
"""

# دالة الترحيب
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحبًا! أنا مساعدك الذكي في مادة الرياضيات 🧠")

# دالة الرد على الرسائل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": pre_prompt},
            {"role": "user", "content": user_message}
        ]
    )
    reply = completion.choices[0].message.content
    await update.message.reply_text(reply, parse_mode="Markdown")

# تشغيل البوت
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()
