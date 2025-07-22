async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.strip().lower()

    # رد ذكي على طلب مسائل نهايات
    if "مسالة" in user_message or "مسألة" in user_message or "نهاية" in user_message or "limit" in user_message:
        await update.message.reply_text(
            "تمام يا نجم، تعالى نركز كده سوا 💪\n\nالسؤال:\nاحسب نهاية الدالة التالية لما x تروح لـ 2:\n\n$$\n\\lim_{x \\to 2} \\frac{x^2 - 4}{x - 2}\n$$",
            parse_mode=telegram.constants.ParseMode.MARKDOWN
        )
        return

    # لو مش مسألة، ابعت لواجهة OpenAI
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": pre_prompt},
            {"role": "user", "content": user_message}
        ]
    )

    reply = completion.choices[0].message["content"]
    await update.message.reply_text(reply, parse_mode=telegram.constants.ParseMode.MARKDOWN)
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import openai
import os
