from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from app.filters.moder import IsModerMessage
from app.keyboards.moder import get_moder_kb


router = Router(name="moder_messages")


@router.message(Command("start"))
async def start_command(message: Message) -> None:
    """
    Эта функция обрабатывает команду /start,
    отправляя приветственное сообщение модератору.

    :param message: Объект Message, представляющий сообщение.
    :return: None

    Внутренний процесс:
    1. Отправляем приветственное сообщение модератору.
    """
    await message.answer(
        "Пока что у тебя есть возможность только отвечать на вопросы в чате",
        reply_markup=get_moder_kb(),
    )


@router.message()
async def echo_message(message: Message) -> None:
    """
    Эта функция обрабатывает любые сообщения, отправленные
    модератором,которые не прошли остальные фильтры.

    :param message: Объект Message, представляющий отправленное сообщение.
    :return: None
    """
    return
