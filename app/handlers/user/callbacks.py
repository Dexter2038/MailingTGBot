from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup

from app.database.actions import add_confirm_user_mailing
from app.keyboards.help import get_help_kb, get_ask_help_kb
from app.states.ask import Ask
from app.states.mail import Mail

router = Router(name=__name__)


@router.callback_query(F.data == "AskQuestionYes")
async def ask_question_yes(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.edit_text(text="Напишите ваш вопрос")
    await state.set_state(Ask.ask)


@router.callback_query(F.data == "AskQuestionNo")
async def ask_question_no(callback: CallbackQuery) -> None:
    await callback.message.edit_text(text="Всего доброго!")


@router.callback_query(F.data == "FAQ")
async def faq(callback: CallbackQuery) -> None:
    kb: InlineKeyboardMarkup = get_help_kb()

    faq_text: str = (
        "Частые вопросы:\n"
        "1. Как пользоваться ботом?\n"
        "Бот реагирует на команды, просмотреть их можно в функциях бота.\n"
        "2. Как я могу задать вопрос?\n"
        "Для этого нужно нажать на кнопку 'Задать вопрос' и подтвердить выбор.\n"
    )

    await callback.message.edit_text(text=faq_text, reply_markup=kb)


@router.callback_query(F.data == "AskQuestion")
async def ask_question(callback: CallbackQuery) -> None:
    kb: InlineKeyboardMarkup = get_ask_help_kb()

    await callback.message.edit_text(text="Вы хотите задать вопрос?", reply_markup=kb)


@router.callback_query(F.data == "ChangeMailNo")
async def change_mail_no(callback: CallbackQuery) -> None:
    await callback.message.edit_text(text="Всего доброго!")


@router.callback_query(F.data == "BotFunctions")
async def bot_functions(callback: CallbackQuery) -> None:
    kb: InlineKeyboardMarkup = get_help_kb()

    await callback.message.edit_text(text="Список функций бота", reply_markup=kb)


@router.callback_query(F.data == "ChangeMailYes")
async def change_mail_yes(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.edit_text(text="Напишите новую почту")
    await state.set_state(state=Mail.change)


@router.callback_query(F.data.startswith("ConfirmMailing_"))
async def confirm_mailing(callback: CallbackQuery) -> None:
    _, mailing_id = callback.data.split("_")
    mailing_id = int(mailing_id)
    user_id: int = callback.from_user.id
    add_confirm_user_mailing(user_id, mailing_id)

    await callback.message.reply(text="Подтверждено!")


@router.callback_query(F.data == "CancelMailing")
async def cancel_mailing(callback: CallbackQuery) -> None:
    await callback.message.reply(text="Отказано!")
