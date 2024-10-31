from aiogram import Bot, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.database.actions import create_user, modify_email
from app.states.ask import Ask
from app.states.start import Start
from app.states.mail import Mail
from app.utils.moders import ask_question
from app.utils.validate_email import validate_email


router = Router(name=__name__)


@router.message(Start.reg)
async def reg(message: Message, state: FSMContext) -> None:
    if not validate_email(email=message.text):
        await message.answer(text="Вы ввели некорректный email. Попробуйте ещё раз")
        return

    if not create_user(
        id=message.from_user.id, email=message.text, username=message.from_user.username
    ):
        await message.answer(text="Произошла ошибка. Попробуйте ещё раз")
        return

    await state.clear()
    await message.answer(text="Вы успешно зарегистрировались!")


@router.message(Mail.change)
async def change_mail(message: Message, state: FSMContext) -> None:
    if not validate_email(email=message.text):
        await message.answer(text="Вы ввели некорректный email. Попробуйте ещё раз")
        return

    if not modify_email(id=message.from_user.id, new_email=message.text):
        await message.answer(text="Произошла ошибка. Попробуйте ещё раз")
        return

    await state.clear()
    await message.answer(text="Вы успешно сменили почту!")


@router.message(Ask.ask)
async def ask(message: Message, state: FSMContext, bot: Bot) -> None:
    if not await ask_question(
        message.chat.id,
        message.from_user.username,
        message.message_id,
        bot,
        message.text,
    ):
        await message.answer(text="Произошла ошибка. Попробуйте позже")
        return

    await message.answer(
        text="Ваш вопрос будет рассмотрен в ближайшее время. Ждите ответа!"
    )
    await state.clear()
