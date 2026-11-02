import asyncio
import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    InlineKeyboardMarkup, 
    InlineKeyboardButton, 
    LabeledPrice, 
    PreCheckoutQuery, 
    Message
)

# 
BOT_TOKEN = "9268992730:AAGzXCI6GVSsvM0Nu8bGpRjS40ITLe105kl"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def get_main_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🧴 Уход за кожей", callback_data="guide_skin"),
            InlineKeyboardButton(text="💇‍♂️ Подбор прически", callback_data="guide_hair")
        ],
        [
            InlineKeyboardButton(text="💪 Осанка и подбородок", callback_data="guide_posture"),
            InlineKeyboardButton(text="👔 Базовый стиль", callback_data="guide_style")
        ],
        [
            InlineKeyboardButton(text="⭐ Купить VIP-Гайд (50 Stars)", callback_data="buy_stars")
        ]
    ])
    return keyboard

@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        f"Привет, {message.from_user.first_name}! 👋\n\n"
        f"Я **GlowMax AI** — твой личный консультант по улучшению внешности (Looksmaxing & Style).\n\n"
        f"Выбери нужный раздел ниже или просто напиши свой вопрос прямо в чат!",
        reply_markup=get_main_keyboard(),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data.startswith("guide_"))
async def process_guides(callback: types.CallbackQuery):
    guide_type = callback.data.split("_")[1]
    
    if guide_type == "skin":
        text = (
            "🧴 **Базовый гайд по уходу за кожей:**\n\n"
            "1. **Умывание:** Используй мягкую пенку/гель утром и вечером.\n"
            "2. **Увлажнение:** Увлажняющий крем каждый день после умывания.\n"
            "3. **Защита (SPF):** Солнцезащитный крем SPF 30/50 ежедневно — главное средство от старения и акне.\n"
            "4. **Питание:** Пей не менее 2л воды в день и уменьши количество сахара."
        )
    elif guide_type == "hair":
        text = (
            "💇‍♂️ **Подбор прически по форме лица:**\n\n"
            "• **Овальное:** Подходит практически любая стрижка (Buzz cut, Fade, Pompadour).\n"
            "• **Квадратное:** Подойдут стрижки с короткими боками и объемом сверху (Crop, Mid Fade).\n"
            "• **Круглое:** Нужен объем сверху и текстура, избегай пышных боков."
        )
    elif guide_type == "posture":
        text = (
            "💪 **Улучшение осанки и линии челюсти:**\n\n"
            "1. **Мьюинг (Mewing):** Держи язык полностью прижатым к нёбу в течение дня.\n"
            "2. **Осанка:** Подбородок слегка назад, лопатки свести и опустить.\n"
            "3. **Сон:** Спи на спине и на низкой подушке для предотвращения отеков."
        )
    elif guide_type == "style":
        text = (
            "👔 **Основа стильного гардероба:**\n\n"
            "• **Базовые цвета:** Черный, белый, серый, темно-синий, бежевый.\n"
            "• **Посадка:** Одежда должна сидеть по фигуре (не слишком обтягивать, но и не висеть мешком).\n"
            "• **Обувь:** Чистые минималистичные белые или черные кеды/кроссовки."
        )
    
    await callback.message.edit_text(text, reply_markup=get_main_keyboard(), parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "buy_stars")
async def send_stars_invoice(callback: types.CallbackQuery):
    await bot.send_invoice(
        chat_id=callback.message.chat.id,
        title="⭐ VIP GlowMax Protocol",
        description="Доступ к эксклюзивному расширенному гайду + индивидуальный разбор внешности.",
        payload="vip_glowmax_pack",
        currency="XTR",
        prices=[
            LabeledPrice(label="VIP Доступ", amount=50)
        ]
    )
    await callback.answer()

@dp.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message(F.successful_payment)
async def process_successful_payment(message: Message):
    await message.answer(
        "🎉 **Оплата прошла успешно!**\n\n"
        "Спасибо за покупку VIP-пакета. Держи ссылку на закрытый эксклюзивный гайд и секретную программу:\n"
        "👉 https://t.me/your_private_channel_link",
        parse_mode="Markdown"
    )

@dp.message()
async def echo_handler(message: Message):
    text = message.text.lower()
    if "привет" in text:
        await message.answer("Привет! Чем могу помочь по уходу за собой или стилю?")
    elif "прыщ" in text or "акне" in text:
        await message.answer("При акне или высыпаниях не выдавливай их! Используй средства с салициловой кислотой (BHA) или цинком.")
    else:
        await message.answer(
            "Я получил твой запрос! Выбери тему из меню ниже или задай более конкретный вопрос по стилю, коже или волосам.",
            reply_markup=get_main_keyboard()
        )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# Запуск крошечного веб-сервера для Render, чтобы он не ругался на порты
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

# Запускаем сервер в фоновом потоке
threading.Thread(target=run_server, daemon=True).start()
