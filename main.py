import os
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# Telegram Bot Token
TOKEN = os.getenv("BOT_TOKEN", "8715110098:AAFBKfysEeaLh94HOu13xEH6t7RBjN6F9XE")

# /start command - နှိပ်ရင် Menu ခလုတ်များ ပေါ်လာမည်
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # စျေးနှုန်း Menu ခလုတ်များ ဖန်တီးခြင်း
    keyboard = [
        [
            InlineKeyboardButton("A - ၁၀၀ ကျပ်", callback_data='price_A'),
            InlineKeyboardButton("B - ၁၀၀ ကျပ်", callback_data='price_B')
        ],
        [
            InlineKeyboardButton("C - ၁၀၀ ကျပ်", callback_data='price_C'),
            InlineKeyboardButton("D - ၁၀၀ ကျပ်", callback_data='price_D')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        "မင်္ဂလာပါခင်ဗျာ။ 👋\n\n"
        "ဝယ်ယူလိုသော ပစ္စည်း သို့မဟုတ် အမျိုးအစားကို အောက်ပါ ခလုတ်များမှ ရွေးချယ်နိုင်ပါတယ်ခင်ဗျာ -\n"
        "(သို့မဟုတ် သင်္ချာတွက်ချက်လိုပါက ဂဏန်းများ တိုက်ရိုက် ရိုက်ထည့်နိုင်ပါတယ်)"
    )
    
    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)

# Button ကို နှိပ်လိုက်သည့်အခါ အကြောင်းပြန်ပေးမည့် စနစ်
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    if data == 'price_A':
        response = "🛒 **Item Telegram Price** ကို ရွေးချယ်ထားပါတယ်ခင်ဗျာ။\n💰 စျေးနှုန်း - **2500 ကျပ်**"
    elif data == 'price_WeChat Price':
        response = "🛒 **Item B** ကို ရွေးချယ်ထားပါတယ်ခင်ဗျာ။\n💰 စျေးနှုန်း - **15000 ကျပ်**"
    elif data == 'price_C':
        response = "🛒 **Item Whatapps price** ကို ရွေးချယ်ထားပါတယ်ခင်ဗျာ။\n💰 စျေးနှုန်း - **2000 ကျပ်**"
    elif data == 'price_D':
        response = "🛒 **Item TikTok Price** ကို ရွေးချယ်ထားပါတယ်ခင်ဗျာ။\n💰 စျေးနှုန်း - **2500 ကျပ်**"
    else:
        response = "အပေါ်က စျေးနှုန်းအတိုင်းပါပဲခဗျ"

    await query.edit_message_text(text=response, parse_mode='Markdown')

# သင်္ချာ တွက်ပေးသည့် စနစ် (Calculator Feature)
async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    
    # ဂဏန်းနှင့် သင်္ချာ သင်္ကေတများ သာ ပါဝင်မှု ရှိ/မရှိ စစ်ဆေးခြင်း
    if not re.match(r'^[0-9+\-*/().\s]+$', text):
        return

    try:
        # သင်္ချာ ပုစ္ဆာ တွက်ချက်ခြင်း
        result = eval(text, {"__builtins__": None}, {})
        await update.message.reply_text(f"🧮 **တွက်ချက်မှု ရလဒ်:**\n`{text}` = **{result}**", parse_mode='Markdown')
    except Exception:
        await update.message.reply_text("⚠️ သင်္ချာ ပုံသေနည်း မှားယွင်းနေပါသည်။ (ဥပမာ- 5+5 သို့မဟုတ် 100*2)")

# Bot စတင် ပတ်မည့် Main Function
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    # Handlers များ ထည့်သွင်းခြင်း
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('menu', start))
    app.add_handler(CallbackQueryHandler(button_click))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), calculate))

    print("Bot is running...")
    app.run_polling()
