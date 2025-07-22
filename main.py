from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحبًا أنا مساعدك الذكي في مادة الرياضيات 🧠📚")

async def plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📘 هذه خطة الدرس:\n1. المفاهيم\n2. الأمثلة\n3. التدريب\n4. التقويم")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.lower()
    if "مثال" in user_message:
        await update.message.reply_text("إليك مثالًا:\nما هو ناتج نهاية الدالة: (x² - 1)/(x - 1) عندما x تقترب من 1؟")
    else:
        await update.message.reply_text("أنا هنا للمساعدة في مادة الرياضيات. جرب مثلاً: /plan")

app = ApplicationBuilder().token("ضع_توكن_البوت_هنا").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("plan", plan))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
