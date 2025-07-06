# main.py

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import BOT_TOKEN, GPT_API_KEY
from technical_analysis import analyze_all, analyze_symbol
import datetime
import openai

bot = telebot.TeleBot(BOT_TOKEN)
openai.api_key = GPT_API_KEY

# 📌 تبدیل ورودی اشتباه به نماد بایننس با GPT
def fix_symbol_with_gpt(user_input):
    prompt = f"""
کاربر نوشته: "{user_input}".
منظور کاربر کدام نماد ارز دیجیتال است؟ فقط نماد بایننس را پاسخ بده، مثلاً BTCUSDT یا ETHUSDT.
اگر مشخص نبود، فقط بنویس: UNKNOWN
    """
    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=10,
        temperature=0.1
    )
    return response.choices[0].text.strip()

# ➕ شروع
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("🟢 ارزهای سودآور", callback_data="profitable"),
        InlineKeyboardButton("🔍 بررسی ارز درخواستی", callback_data="custom")
    )
    bot.send_message(message.chat.id, "یکی از گزینه‌های زیر را انتخاب کنید:", reply_markup=markup)

# ✅ هندل دکمه‌ها
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "profitable":
        bot.send_message(call.message.chat.id, "🔄 در حال بررسی ارزهای سودآور...")
        from technical_analysis import analyze_symbol
        result = analyze_symbol("BTCUSDT")
        results = [result] if result else []

        now = datetime.datetime.now().strftime("%H:%M")
        if results:
            for res in results[:5]:
                msg = (
                    f"📈 اسم ارز: {res['symbol']}\n"
                    f"💰 قیمت ارز: {res['price']} USDT\n"
                    f"🔼 درصد سود احتمالی: {res['profit_chance']}%\n"
                    f"🔽 درصد ضرر احتمالی: {res['loss_chance']}%\n"
                    f"⏱ تایم فریم: 30 دقیقه\n"
                    f"🕐 ساعت استعلام: {now}"
                )
                bot.send_message(call.message.chat.id, msg)
        else:
            bot.send_message(call.message.chat.id, "هیچ ارز سودآوری یافت نشد.")

    elif call.data == "custom":
        msg = bot.send_message(call.message.chat.id, "نماد یا اسم ارز مورد نظر را وارد کنید:")
        bot.register_next_step_handler(msg, handle_custom_symbol)

    elif call.data == "back":
        send_welcome(call.message)

# 📌 بررسی ارز کاربر
def handle_custom_symbol(message):
    user_input = message.text.strip()
    fixed_symbol = fix_symbol_with_gpt(user_input)
    if fixed_symbol.upper() == "UNKNOWN":
        bot.send_message(message.chat.id, "❌ نتونستم نماد رو تشخیص بدم.")
        return

    result = analyze_symbol(fixed_symbol)
    if not result:
        bot.send_message(message.chat.id, "❌ خطا در تحلیل این ارز.")
        return

    now = datetime.datetime.now().strftime("%H:%M")
    msg = (
        f"📈 اسم ارز: {result['symbol']}\n"
        f"💰 قیمت ارز: {result['price']} USDT\n"
        f"🔼 درصد سود احتمالی: {result['profit_chance']}%\n"
        f"🔽 درصد ضرر احتمالی: {result['loss_chance']}%\n"
        f"⏱ تایم فریم: 30 دقیقه\n"
        f"🕐 ساعت استعلام: {now}"
    )
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔙 بازگشت", callback_data="back"))
    bot.send_message(message.chat.id, msg, reply_markup=markup)

# ▶ شروع ربات
bot.polling()
