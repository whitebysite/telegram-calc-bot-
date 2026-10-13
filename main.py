import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    
    allowed_chars = set("0123456789+-*/.() ")
    if all(char in allowed_chars for char in text) and any(op in text for op in "+-*/"):
        try:
            result = eval(text)
            await update.message.reply_text(f"🧮 ဖြေရှင်းချက်: {text} = *{result}*", parse_mode="Markdown")
        except Exception:
            await update.message.reply_text("❌ မှားယွင်းနေသော ညီမျှခြင်း ဖြစ်ပါသည်။ (ဥပမာ: 5+5 သို့မဟုတ် 10*2)")
    else:
        await update.message.reply_text("မင်္ဂလာပါ! ကျေးဇူးပြု၍ တွက်ချက်လိုသော ပုံစံရေးပါ။ (ဥပမာ: 15 + 25 သို့မဟုတ် 50 * 2)")

if __name__ == '__main__':
    BOT_TOKEN = "8715110098:AAFBKfysEeaLh94HOu13xEH6t7RBjN6F9XE"
    
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, calculate))

    print("Calculator Bot စတင် အလုပ်လုပ်နေပါပြီ...")
    app.run_polling()
