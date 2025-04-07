import asyncio
import types
import emoji
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import message, KeyboardButton, ReplyKeyboardMarkup, FSInputFile, CallbackQuery
from aiogram.filters.command import Command
import random
import os
from aiogram.fsm.state import State, StatesGroup
from kots import make_graph

class GameState(StatesGroup):
    waiting_for_answer = State()

load_dotenv()
TELEGRAM_API_KEY = os.getenv('TELEGRAM_API_KEY')
bot = Bot(token=TELEGRAM_API_KEY)
dp = Dispatcher()


@dp.message(Command('start'))
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


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())