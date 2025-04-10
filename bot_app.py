import os
import json
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from dotenv import load_dotenv
import db

load_dotenv()
bot = Bot(token=os.getenv("TELEGRAM_API_KEY"))
dp = Dispatcher()

# === AIOHTTP SERVER ===

async def index(request):
    return web.FileResponse('./html_dir/bot_app.html')

# API endpoint: check_user
async def check_user(request):
    try:
        data = await request.json()
        user_id = int(data.get("user_id"))
        username = data.get("username")

        db.get_or_create_user(user_id, username)
        can_request = db.can_user_request(user_id)
        score = db.get_score(user_id)

        response = {
            "username": username,
            "points": score,
            "attempts_today": db.get_requests_today(user_id),
            "limit_reached": not can_request
        }
        return web.json_response(response)

    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)

# === TELEGRAM HANDLER ===

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [types.KeyboardButton(text="Открыть WebApp", web_app=types.WebAppInfo(url="https://web-production-1d265.up.railway.app/"))]
    ])
    await message.answer("Привет! Нажми кнопку ниже:", reply_markup=kb)

# === APP SETUP ===

app = web.Application()
app.router.add_get("/", index)
app.router.add_post("/api/check_user", check_user)
app.router.add_static('/html_dir/', path='html_dir', name='html_dir')

async def on_startup(app):
    import asyncio
    asyncio.create_task(dp.start_polling(bot))

app.on_startup.append(on_startup)

if __name__ == "__main__":
    web.run_app(app, port=int(os.getenv("PORT", 8080)))
