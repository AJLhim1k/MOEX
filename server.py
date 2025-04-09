from aiohttp import web
import aiosqlite
from datetime import date

async def get_user_info(request):
    user_id = request.query.get("user_id")
    if not user_id:
        return web.json_response({"error": "user_id required"}, status=400)

    async with aiosqlite.connect("db.sqlite") as db:
        async with db.execute("SELECT username, score, daily_requests, last_request FROM users WHERE user_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()

        today = str(date.today())

        if row:
            username, score, daily_requests, last_request = row

            if last_request != today:
                daily_requests = 0
                async with db.execute("""
                    UPDATE users SET daily_requests = 0, last_request = ? WHERE user_id = ?
                """, (today, user_id)):
                    await db.commit()
        else:
            username = f"User_{user_id}"
            score = 100
            daily_requests = 0
            await db.execute("""
                INSERT INTO users (user_id, username, score, daily_requests, last_request)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, username, score, daily_requests, today))
            await db.commit()

        return web.json_response({
            "username": username,
            "score": score,
            "daily_requests": daily_requests
        })

app = web.Application()
app.router.add_get("/get_user_info", get_user_info)

if __name__ == '__main__':
    web.run_app(app, port=8000)
