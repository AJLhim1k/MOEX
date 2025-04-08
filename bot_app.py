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

from bot import GameState
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
                    web_app=WebAppInfo(url='https://ajlhim1k.github.io/MOEX/bot_app.html'))
            ]
        ],
        resize_keyboard=True
    )
    await message.answer("sdgsdfgsdf", reply_markup=markup)


@dp.message(Command('викторина'))
async def send_welcome(message: message, state: FSMContext):
    kb = [
        [KeyboardButton(text="Long shares", )],
        [KeyboardButton(text="Short shares")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="Хмм...")
    _, _, files = next(os.walk(".\questions"))
    file_count = len(files) + 99
    pic = random.randint(100, file_count)
    make_graph(pic, "q")
    await state.update_data(current_pic=pic)
    await message.answer_photo(photo=FSInputFile(f'.\questions\plot{pic}.png'), caption="Начнем игру!\nОпредели, есть ли на данном графике манипуляуция?", reply_markup=keyboard)
    await state.set_state(GameState.waiting_for_answer)


@dp.message(GameState.waiting_for_answer)
async def handle_answer(message: message, state: FSMContext):
    kb = [
        [KeyboardButton(text="Я молодец..?", )],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="Хмм...")
    data = await state.get_data()
    pic = data.get("current_pic")
    make_graph(pic, "ans")
    await state.update_data(current_pic=pic)
    user_response = message.text
    if user_response == "Long shares":
        kb = [
            [KeyboardButton(text="Круто! Назад в меню", )],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="Хмм...")
        await message.answer_photo(photo=FSInputFile(f'.\\answers\plot{pic}.png'), caption="Молодец, ты был прав!", reply_markup=keyboard)
    elif user_response == "Short shares":
        kb = [
            [KeyboardButton(text="Плаки-плаки, назад в меню", )],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="Хмм...")
        await message.answer_photo(photo=FSInputFile(f'.\\answers\plot{pic}.png'), caption="Нет", reply_markup=keyboard)



@dp.message(F.text.lower() == "викторина")
async def handle_webapp_viktorina(message: types.Message, state: FSMContext):
    await send_welcome(message, state)


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())