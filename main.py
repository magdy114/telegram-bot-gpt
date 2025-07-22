import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

BOT_TOKEN = "8069508243:AAH9yMewI2BXe2v55M3z-ex5UwwF-s4XJns"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("مرحبًا، أنا مساعدك الذكي في مادة الرياضيات 🧠📚")

async def plan_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("📘 هذه خطة الدرس: \n1. المفاهيم\n2. الأمثلة\n3. التدريب\n4. التقويم")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.message.text.lower()
    if "نهاية" in msg or "النهايات" in msg:
        await update.message.reply_text("📌 النهاية هي القيمة التي تقترب منها الدالة عندما تقترب x من قيمة معينة.")
    else:
        await update.message.reply_text("أنا هنا للمساعدة في مادة الرياضيات. جرّب مثلاً: /plan")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("plan", plan_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == "__main__":
    main()
from telegram.ext import MessageHandler, filters

# تابع جديد للتعامل مع الرسائل النصية مثل "أعطني مثال"
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if "مثال" in text:
        await update.message.reply_text("📌 مثال على خطة الدرس:\n1. مراجعة المفاهيم\n2. حل تمرينات\n3. تطبيق واقعي\n4. تقويم سريع")
    else:
        await update.message.reply_text("أنا هنا للمساعدة في مادة الرياضيات. جرب أمرًا مثل /plan")

# أضف هذا الهاندلر في `main()` داخل التطبيق
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
