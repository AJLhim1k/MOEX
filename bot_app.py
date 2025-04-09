import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from aiogram.filters.command import Command
from dotenv import load_dotenv
import os
import sqlite3
from datetime import datetime

load_dotenv()
TELEGRAM_API_KEY = os.getenv('TELEGRAM_API_KEY')

bot = Bot(token=TELEGRAM_API_KEY)
dp = Dispatcher()

def get_user_data(user_id, username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    today = datetime.now().strftime('%Y-%m-%d')

    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    row = cursor.fetchone()

    if not row:
        cursor.execute(
            "INSERT INTO users (user_id, username, score, request_date, request_count) VALUES (?, ?, ?, ?, ?)",
            (user_id, username, 100, today, 0)
        )
        conn.commit()
        conn.close()
        return (100, 0, today)

    score, request_count, request_date = row[2], row[4], row[3]

    if request_date != today:
        request_count = 0
        cursor.execute("UPDATE users SET request_date=?, request_count=0 WHERE user_id=?",
                       (today, user_id))
        conn.commit()

    conn.close()
    return (score, request_count, today)

@dp.message(Command('start'))
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username or "Без ника"

    score, count, today = get_user_data(user_id, username)

    reply_markup = ReplyKeyboardMarkup(
        keyboard=[[
            KeyboardButton(
                text='Играть',
                web_app=WebAppInfo(url=f'https://ajlhim1k.github.io/MOEX/html_dir/bot_app.html?score={score}&count={count}')
            )
        ]],
        resize_keyboard=True
    )
    await message.answer(f"Привет, {username}!\nУ тебя {score} баллов.\nСегодня ты использовал {count}/5 попыток.", reply_markup=reply_markup)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
