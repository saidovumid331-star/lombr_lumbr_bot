import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiohttp import web

# BOT TOKENINI SHU YERGA QO'YING
BOT_TOKEN = "8869987652:AAH1F9g00wpX2IgoGTXww9eRLLZ9ng70gfw" 
web.Application()

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Kalkulyator tugmalarini yasash funksiyasi
def get_calculator_keyboard(product_name: str, current_num: str):
    builder = InlineKeyboardBuilder()
    display_num = current_num if current_num else "0"
    
    # 1-qator: Ekranda yig'ilayotgan sonni ko'rsatish
    builder.row(types.InlineKeyboardButton(text=f"🔢 Miqdor: {display_num}", callback_data="ignore"))
    
    # Sonli tugmalar (Kalkulyator ko'rinishida)
    builder.row(
        types.InlineKeyboardButton(text="1", callback_data=f"num:{product_name}:{current_num}:1"),
        types.InlineKeyboardButton(text="2", callback_data=f"num:{product_name}:{current_num}:2"),
        types.InlineKeyboardButton(text="3", callback_data=f"num:{product_name}:{current_num}:3")
    )
    builder.row(
        types.InlineKeyboardButton(text="4", callback_data=f"num:{product_name}:{current_num}:4"),
        types.InlineKeyboardButton(text="5", callback_data=f"num:{product_name}:{current_num}:5"),
        types.InlineKeyboardButton(text="6", callback_data=f"num:{product_name}:{current_num}:6")
    )
    builder.row(
        types.InlineKeyboardButton(text="7", callback_data=f"num:{product_name}:{current_num}:7"),
        types.InlineKeyboardButton(text="8", callback_data=f"num:{product_name}:{current_num}:8"),
        types.InlineKeyboardButton(text="9", callback_data=f"num:{product_name}:{current_num}:9")
    )
    builder.row(
        types.InlineKeyboardButton(text="0", callback_data=f"num:{product_name}:{current_num}:0"),
        types.InlineKeyboardButton(text="❌ Tozalash", callback_data=f"clear:{product_name}")
    )
    # Eng oxirida Yuborish (Tasdiqlash) tugmasi
    builder.row(
        types.InlineKeyboardButton(text="🚀 Buyurtmani yuborish", callback_data=f"send:{product_name}:{current_num}")
    )
    
    return builder.as_markup()

# /start buyrug'i kelganda
@dp.message(CommandStart())
async def start_command(message: types.Message):
    kb = [
        [types.KeyboardButton(text="🛒 Menyu"), types.KeyboardButton(text="ℹ️ Biz haqimizda")],
        [types.KeyboardButton(text="📞 Kontakt")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="Bo'limni tanlang...")
    await message.answer(f"Assalomu alaykum, {message.from_user.full_name}!\nBotimizga xush kelibsiz!", reply_markup=keyboard)

# "🛒 Menyu" bosilganda
@dp.message(F.text == "🛒 Menyu")
async def menu_handler(message: types.Message):
    menu_kb = [
        [types.KeyboardButton(text="🍔 Fast Food"), types.KeyboardButton(text="🍹 Ichimliklar")],
        [types.KeyboardButton(text="⬅️ Ortga")]
    ]
    menu_keyboard = types.ReplyKeyboardMarkup(keyboard=menu_kb, resize_keyboard=True)
    await message.answer("Kategoriyalardan birini tanlang:", reply_markup=menu_keyboard)

# 🍔 Fast Food bo'limi
@dp.message(F.text == "🍔 Fast Food")
async def fastfood_handler(message: types.Message):
    fastfood_kb = [
        [types.KeyboardButton(text="🫔 Lavash"), types.KeyboardButton(text="🍔 Burger")],
        [types.KeyboardButton(text="🌭 Hot-dog")],
        [types.KeyboardButton(text="⬅️ Ortga")]
    ]
    fastfood_keyboard = types.ReplyKeyboardMarkup(keyboard=fastfood_kb, resize_keyboard=True)
    await message.answer("Taomlardan birini tanlang:", reply_markup=fastfood_keyboard)

# 🍹 Ichimliklar bo'limi
@dp.message(F.text == "🍹 Ichimliklar")
async def drinks_handler(message: types.Message):
    drinks_kb = [
        [types.KeyboardButton(text="🥤 Coca-Cola"), types.KeyboardButton(text="🍊 Fanta")],
        [types.KeyboardButton(text="🧃 Tabiiy sharbat")],
        [types.KeyboardButton(text="⬅️ Ortga")]
    ]
    drinks_keyboard = types.ReplyKeyboardMarkup(keyboard=drinks_kb, resize_keyboard=True)
    await message.answer("Ichimliklardan birini tanlang:", reply_markup=drinks_keyboard)

# Taom yoki ichimlik ustiga bosilganda kalkulyator chiqarish
@dp.message(F.text.in_({"🫔 Lavash", "🍔 Burger", "🌭 Hot-dog", "🥤 Coca-Cola", "🍊 Fanta", "🧃 Tabiiy sharbat"}))
async def product_handler(message: types.Message):
    product_name = message.text
    await message.answer(
        f"Siz [{product_name}] tanladingiz.\n\nNechta buyurtma qilasiz? Quyidagi paneldan sonlarni terib, keyin yuborish tugmasini bosing:",
        reply_markup=get_calculator_keyboard(product_name, "")
    )

# Raqamlar bosilganda sonni yonma-yon yozish (yig'ish)
@dp.callback_query(F.data.startswith("num:"))
async def num_callback(call: types.CallbackQuery):
    _, product_name, current_num, clicked_digit = call.data.split(":")
    
    if current_num == "" and clicked_digit == "0":
        await call.answer()
        return
        
    new_num = current_num + clicked_digit
    await call.message.edit_reply_markup(reply_markup=get_calculator_keyboard(product_name, new_num))
    await call.answer()

# Tozalash tugmasi bosilganda
@dp.callback_query(F.data.startswith("clear:"))
async def clear_callback(call: types.CallbackQuery):
    _, product_name = call.data.split(":")
    await call.message.edit_reply_markup(reply_markup=get_calculator_keyboard(product_name, ""))
    await call.answer()

# Buyurtmani yuborish tugmasi bosilganda
@dp.callback_query(F.data.startswith("send:"))
async def send_callback(call: types.CallbackQuery):
    _, product_name, final_num = call.data.split(":")
    
    if not final_num:
        await call.answer("Iltimos, oldin miqdorni tering!", show_alert=True)
        return
        
    await call.message.edit_text(f"✅ {final_num} ta {product_name} savatga qo'shildi!\n\nBuyurtma muvaffaqiyatli qabul qilindi.")
    await call.answer()

# ⬅️ Ortga tugmasi
@dp.message(F.text == "⬅️ Ortga")
async def back_handler(message: types.Message):
    kb = [[types.KeyboardButton(text="🛒 Menyu"), types.KeyboardButton(text="ℹ️ Biz haqimizda")], [types.KeyboardButton(text="📞 Kontakt")]]
    await message.answer("Bosh menyuga qaytdingiz:", reply_markup=types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True))

# ℹ️ Biz haqimizda bo'limi
@dp.message(F.text == "ℹ️ Biz haqimizda")
async def about_handler(message: types.Message):
    await message.answer("ℹ️ Bu bot raqamli xizmatlarni avtomatlashtirish uchun ishlab chiqildi.")

# 📞 Kontakt bo'limi
@dp.message(F.text == "📞 Kontakt")
async def contact_handler(message: types.Message):
    await message.answer("📞 Biz bilan bog'lanish uchun admin: @shaxsiy_profilingiz")

# Echo handler
@dp.message()
async def echo_handler(message: types.Message):
    await message.answer(f"Siz yozdingiz: {message.text}\n\nIltimos, pastdagi tugmalardan foydalaning.")


# --- RENDER SERVER UCHUN VEB-SAHIFA QISMI ---

async def handle(request):
    return web.Response(text="Bot 24/7 rejimda muvaffaqiyatli ishlayapti!")

async def main():
    port = int(os.environ.get("PORT", 10000))
    
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()

    print(f"Veb-server {port}-portda ishga tushdi...")
    print("Bot polling rejimida faollashtirildi...")
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
