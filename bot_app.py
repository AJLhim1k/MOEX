import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, WebAppInfo

load_dotenv()
TELEGRAM_API_KEY = os.getenv('TELEGRAM_API_KEY')

bot = Bot(token=TELEGRAM_API_KEY)
dp = Dispatcher()

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    markup = ReplyKeyboardMarkup(
        keyboard=[[
            KeyboardButton(
                text='Играть',
                web_app=WebAppInfo(url='https://ajlhim1k.github.io/MOEX/html_dir/bot_app.html')
            )
        ]],
        resize_keyboard=True
    )
    await message.answer("Привет! Начнем игру?", reply_markup=markup)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
