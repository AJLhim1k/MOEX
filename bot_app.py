import asyncio
import os
import sqlite3
from datetime import datetime
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
bot = Bot(token=os.getenv("TELEGRAM_API_KEY"))
dp = Dispatcher()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

DB_PATH = "users.db"

def init_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        points INTEGER DEFAULT 100,
        attempts_today INTEGER DEFAULT 0,
        last_attempt_date TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()

@dp.message(Command("start"))
async def start_handler(message: types.Message, state: FSMContext):
    markup = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Играть", web_app=WebAppInfo(url="https://ajlhim1k.github.io/MOEX/html_dir/bot_app.html"))]],
        resize_keyboard=True
    )
    await message.answer("Привет! Готов сыграть?", reply_markup=markup)

@app.post("/check_user/")
async def check_user(request: Request):
    data = await request.json()
    user_id = int(data.get("user_id"))
    username = data.get("username")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    row = cur.fetchone()

    today = datetime.now().strftime("%Y-%m-%d")

    if row:
        last_date = row[4]
        if last_date != today:
            cur.execute("UPDATE users SET attempts_today = 0, last_attempt_date = ? WHERE user_id = ?", (today, user_id))
            conn.commit()
        cur.execute("SELECT points, attempts_today FROM users WHERE user_id = ?", (user_id,))
        points, attempts_today = cur.fetchone()
    else:
        cur.execute("INSERT INTO users (user_id, username, points, attempts_today, last_attempt_date) VALUES (?, ?, ?, ?, ?)",
                    (user_id, username, 100, 0, today))
        conn.commit()
        points = 100
        attempts_today = 0

    conn.close()

    if attempts_today >= 5:
        return JSONResponse(content={"limit_reached": True})
    else:
        return JSONResponse(content={"username": username, "points": points, "attempts_today": attempts_today})

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(dp.start_polling(bot))
