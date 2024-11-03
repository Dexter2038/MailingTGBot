import asyncio
from os import environ
from aiogram import Bot, Dispatcher
from app.database.models import init_db
from app.handlers import get_router

init_db()


bot = Bot(token=environ["BOT_TOKEN"])

dp = Dispatcher()

dp.include_router(get_router())

asyncio.new_event_loop().run_until_complete(dp.start_polling(bot))
