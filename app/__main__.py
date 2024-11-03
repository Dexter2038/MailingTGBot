import asyncio
from os import environ
from aiogram import Bot, Dispatcher
from app.config.init import initialize_app
from app.handlers import get_router

initialize_app()

try:
    bot = Bot(token=environ["BOT_TOKEN"])
except KeyError:
    raise Exception("Переменная окружения 'BOT_TOKEN' не найдена")
except Exception as e:
    raise e

dp = Dispatcher()

dp.include_router(get_router())

asyncio.new_event_loop().run_until_complete(dp.start_polling(bot))
