import os
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from dotenv import load_dotenv

load_dotenv()
bot = Bot(token=os.getenv("TELEGRAM_API_KEY"))
dp = Dispatcher()

# AIOHTTP server for static HTML
async def index(request):
    return web.FileResponse('./html_dir/bot_app.html')

app = web.Application()
app.router.add_get('/', index)
app.router.add_static('/html_dir/', path='html_dir', name='html_dir')

# Telegram command handler
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [types.KeyboardButton(text="Открыть WebApp", web_app=types.WebAppInfo(url="https://web-production-1d265.up.railway.app/"))]
    ])
    await message.answer("Привет! Нажми кнопку ниже:", reply_markup=kb)

# Запуск Telegram и Web сервера
async def on_startup(app):
    import asyncio
    asyncio.create_task(dp.start_polling(bot))

app.on_startup.append(on_startup)

if __name__ == '__main__':
    web.run_app(app, port=int(os.getenv('PORT', 8080)))
