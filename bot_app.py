import asyncio
import types
import emoji
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import message, KeyboardButton, ReplyKeyboardMarkup, FSInputFile, CallbackQuery, WebAppInfo
from aiogram.types.web_app_info import WebAppInfo
from aiogram.filters.command import Command
import random
import os
from aiogram.fsm.state import State, StatesGroup
from kots import make_graph

load_dotenv()
TELEGRAM_API_KEY = os.getenv('TELEGRAM_API_KEY')
bot = Bot(token=TELEGRAM_API_KEY)
dp = Dispatcher()


@dp.message(Command('start'))
async def send_welcome(message: types.Message):
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text='gfdgerg',
                    web_app=WebAppInfo(url='http://wiki.cs.hse.ru/Заглавная_страница'))
            ]
        ],
        resize_keyboard=True
    )
    await message.answer("sdgsdfgsdf", reply_markup=markup)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())