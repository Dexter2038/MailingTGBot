from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.keyboards.user import get_user_kb


router = Router(name="user_messages")


@router.message(Command("start"))
async def start_command(message: Message):
    """
    Обработчик команды /start для пользователей.

    :param message: Новое сообщение, которое пришло от пользователя.
    """
    await message.answer(
        f"Добро пожаловать, @{message.from_user.username}!", reply_markup=get_user_kb()
    )
