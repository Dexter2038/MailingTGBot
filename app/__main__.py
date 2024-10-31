from app.config import init_config
from app.database.actions import add_confirm, get_all_confirms

init_config()

import asyncio
from os import environ
from aiogram import Bot, Dispatcher
from app.handlers import get_router

print(add_confirm(text="Мы тут ебали вас"))
add_confirm(text="Короче мы тут ебали вас"[:125])
text = "Сделал, при вступлении юзера в чат модеров, бот видит это и добавляет его, потому что так бот может и сохранить username (который @) вместе с id модератора, а админ получается добавлять не может внутри бота, а добавляя юзеров в чат. Если кто-то выходит, он это тоже видит и убирает его из модеров. За то админ может контролировать модеров, и видеть не просто их id, а ещё и username'ы, но управлять их уровнями и исключать их может"
print(add_confirm(text=text[:125]))

for confirm in get_all_confirms():
    _id, text = confirm

    print(f"Подтверждение {_id}: {text}")

pass

try:
    bot = Bot(token=environ["BOT_TOKEN"])
except KeyError as e:
    print("Не нашли переменную окружения 'BOT_TOKEN'")
    exit(code=403)

router = get_router()

dp = Dispatcher()

dp.include_router(router)

asyncio.get_event_loop().run_until_complete(dp.start_polling(bot))
