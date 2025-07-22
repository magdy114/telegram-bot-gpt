import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import matplotlib.pyplot as plt
import io
import numpy as np

BOT_TOKEN = "8069508243:AAGvquW-VEvBgJZQsxOlGHKz1XyYCHvczbw"

# إعداد اللوجات
logging.basicConfig(level=logging.INFO)

# دالة توليد رسم بياني بسيط
def generate_plot():
    x = np.linspace(-10, 10, 100)
    y = x ** 2
    plt.figure()
    plt.plot(x, y)
    plt.title("رسم دالة تربيعية")
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf

# الرد على الرسائل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if "مسالة" in text or "مسألة" in text:
        response = (
            "تمام يا نجم، تعالى نبدأ بمسألة نهايات 💪\n"
            "السؤال:\n"
            "احسب نهاية الدالة التالية لما x تروح لـ 3:\n\n"
            "$$\n\\lim_{x \\to 3} \\frac{x^2 - 9}{x - 3}\n$$"
        )
        await update.message.reply_text(response, parse_mode="MarkdownV2")

    elif "رسم" in text:
        await update.message.reply_text("ثواني وهبعتلك الرسم البياني ✍️...")
        buf = generate_plot()
        await update.message.reply_photo(photo=buf)

    elif "شرح" in text:
        await update.message.reply_text(
            "تمام يا نجم، تعالى نركز كده سوا 💪\n"
            "النهاية هي قيمة الدالة لما المتغير يقرب من رقم معين.\n"
            "يعني بنشوف: لو قربنا من الرقم ده من ناحيتي اليمين والشمال، هل الناتج بيكون نفس القيمة؟"
        )

    else:
        await update.message.reply_text("أنا جاهز أساعدك في الرياضيات 💡 ابعتلي كلمة 'مسألة' أو 'رسم' أو 'شرح'")

# تشغيل البوت
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 البوت شغال دلوقتي...")
    app.run_polling()
