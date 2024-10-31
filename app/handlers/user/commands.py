from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup

from app.database.actions import get_email_by_id, is_user_registered
from app.keyboards.help import get_help_kb
from app.keyboards.mail import get_mail_kb
from app.states.ask import Ask
from app.states.start import Start


router = Router(name=__name__)


@router.message(Command("start"))
async def start_command(message: Message, state: FSMContext) -> None:
    if is_user_registered(id=message.from_user.id):
        await message.answer(
            text="Добро пожаловать! Чтобы узнать команды введите /help"
        )
        return

    await state.set_state(state=Start.reg)
    await message.answer(text="Для регистрации введите свой email")


@router.message(Command("help"))
async def help_command(message: Message) -> None:
    kb: InlineKeyboardMarkup = get_help_kb()

    await message.answer(
        text="Нажмите на кнопку ниже для получения помощи", reply_markup=kb
    )


@router.message(Command("mail"))
async def mail_command(message: Message) -> None:
    kb: InlineKeyboardMarkup = get_mail_kb()

    await message.answer(text="Вы хотите сменить почту?", reply_markup=kb)


@router.message(Command("mymail"))
async def mymail_command(message: Message) -> None:
    email: str = get_email_by_id(id=message.from_user.id)

    await message.answer(text=f"Ваша почта: {email}")


@router.message(Command("rules"))
async def rules_command(message: Message) -> None:
    await message.answer(text="Тут будет правила")


@router.message(Command("about"))
async def about_command(message: Message) -> None:
    await message.answer(text="Тут будет информация о боте")


@router.message(Command("ask"))
async def ask_command(message: Message, state: FSMContext) -> None:
    await message.answer(text="Напишите ваш вопрос")
    await state.set_state(state=Ask.ask)


@router.message(Command("faq"))
async def faq_command(message: Message) -> None:
    await message.answer(text="Тут будет FAQ")


@router.message(Command("myid"))
async def myid_command(message: Message) -> None:
    await message.answer(text=f"Ваш ID: {message.from_user.id}")


@router.message(Command("myusername"))
async def myusername_command(message: Message) -> None:
    await message.answer(text=f"Ваш username: {message.from_user.username}")
