from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.keyboards.user import get_user_kb


router = Router(name="user_messages")


@router.message(Command("start"))
async def start_command(message: Message, state: FSMContext) -> None:
    """
    Обработчик команды /start для пользователей.

    :param message: Новое сообщение, которое пришло от пользователя.
    """

    await state.clear()
    await message.answer(
        f"Добро пожаловать, @{message.from_user.username}!", reply_markup=get_user_kb()
    )


@router.message()
async def echo_message(message: Message, state: FSMContext) -> None:
    """
    Обработчик любых сообщений для пользователей,
    которые не прошли остальные фильтры.

    :param message: Новое сообщение, которое пришло от пользователя.
    """

    await state.clear()
    await message.answer(
        f"Добро пожаловать, @{message.from_user.username}!", reply_markup=get_user_kb()
    )
