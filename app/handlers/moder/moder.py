from typing import List
from aiogram import F, Bot, Router
from aiogram.filters import Command, CommandObject, and_f
from aiogram.types import Message, CallbackQuery

from app.filters.moder import IsModer


router = Router(name=__name__)


@router.message(
    and_f(IsModer(), F.reply_to_message, F.reply_to_message.text.startswith("Вопрос["))
)
async def answer_question(message: Message, bot: Bot) -> None:
    # Пример reply_to_message.text: "Вопрос[<chat_id>, <msg_id>] <question>"
    # Получаем данные задающего вопрос
    data: str = message.reply_to_message.text.split("]", 1)[0][7:].split(", ")

    # Получаем chat_id и msg_id задающего вопрос
    chat_id, msg_id = list(map(int, data))

    await message.reply_to_message.delete()

    await bot.send_message(
        chat_id,
        message.text
        + "\n\nНа вопрос ответил модератор %s" % message.from_user.username,
        reply_to_message_id=msg_id,
    )
