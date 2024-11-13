from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.states.admin import Admin

from app.handlers.functions.admin.states import *


router = Router(name="root_states")


@router.message(Admin.ask_question)
async def ask_question_state_root(
    message: Message, state: FSMContext, bot: Bot
) -> None:
    await ask_question_state(message, state, bot)


@router.message(Admin.add_moderator)
async def add_moder_state_root(message: Message, state: FSMContext) -> None:
    await add_moder_state(message, state)


@router.message(Admin.add_subadmin)
async def add_subadmin_state_root(message: Message, state: FSMContext) -> None:
    await add_subadmin_state(message, state)


@router.message(Admin.make_mailing)
async def make_mailing_state_root(
    message: Message, state: FSMContext, bot: Bot
) -> None:
    await make_mailing_state(message, state, bot)


@router.message(Admin.add_news)
async def add_news_state_root(message: Message, state: FSMContext) -> None:
    await add_news_state(message, state)


@router.message(Admin.add_quiz)
async def add_quiz_state_root(message: Message, state: FSMContext) -> None:
    await add_quiz_state(message, state)


@router.message(Admin.add_confirm)
async def add_confirm_state_root(message: Message, state: FSMContext) -> None:
    await add_confirm_state(message, state)


@router.message(Admin.edit_about_quiz)
async def edit_about_quiz_state_root(message: Message, state: FSMContext) -> None:
    await edit_about_quiz_state(message, state)


@router.message(Admin.edit_faq)
async def edit_faq_state_root(message: Message, state: FSMContext) -> None:
    await edit_faq_state(message, state)


@router.message(Admin.edit_news)
async def edit_news_state_root(message: Message, state: FSMContext) -> None:
    await edit_news_state(message, state)


@router.message(Admin.edit_quiz)
async def edit_quiz_state_root(message: Message, state: FSMContext) -> None:
    await edit_quiz_state(message, state)


@router.message(Admin.edit_rules)
async def edit_rules_state_root(message: Message, state: FSMContext) -> None:
    await edit_rules_state(message, state)
