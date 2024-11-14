from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext


from app.handlers.functions.admin.callbacks import *


router = Router(name="root_callbacks")


@router.callback_query(F.data == "user_mode")
async def user_mode_callback_root(callback: CallbackQuery) -> None:
    await user_mode_callback(callback)


@router.callback_query(F.data == "about_quiz_user")
async def about_quiz_user_callback_root(callback: CallbackQuery) -> None:
    await about_quiz_user_callback(callback)


@router.callback_query(F.data == "faq_user")
async def faq_user_callback_root(callback: CallbackQuery) -> None:
    await faq_user_callback(callback)


@router.callback_query(F.data == "quizzes_user")
async def quizzes_user_callback_root(callback: CallbackQuery) -> None:
    await quizzes_user_callback(callback)


@router.callback_query(F.data == "news_user")
async def news_user_callback_root(callback: CallbackQuery) -> None:
    await news_user_callback(callback)


@router.callback_query(F.data == "rules_user")
async def rules_user_callback_root(callback: CallbackQuery) -> None:
    await rules_user_callback(callback)


@router.callback_query(F.data == "ask_question_user")
async def ask_question_user_callback_root(
    callback: CallbackQuery, state: FSMContext
) -> None:
    await ask_question_user_callback(callback, state)


@router.callback_query(F.data == "show_moders")
async def show_moders_callback_root(callback: CallbackQuery, state: FSMContext) -> None:
    await show_moders_callback(callback, state)


@router.callback_query(F.data.startswith("moder_"))
async def show_moder_callback_root(callback: CallbackQuery, state: FSMContext) -> None:
    await show_moder_callback(callback, state)


@router.callback_query(F.data.startswith("del_moder_"))
async def del_moder_callback_root(callback: CallbackQuery, state: FSMContext) -> None:
    await del_moder_callback(callback, state)


@router.callback_query(F.data == "add_moderator")
async def add_moderator_callback_root(
    callback: CallbackQuery, state: FSMContext
) -> None:
    await add_moderator_callback(callback, state)


@router.callback_query(F.data == "show_subadmins")
async def show_subadmins_callback_root(
    callback: CallbackQuery, state: FSMContext
) -> None:
    await show_subadmins_callback(callback, state)


@router.callback_query(F.data.startswith("subadmin_"))
async def show_subadmin_callback_root(
    callback: CallbackQuery, state: FSMContext
) -> None:
    await show_subadmin_callback(callback, state)


@router.callback_query(F.data.startswith("del_subadmin_"))
async def del_subadmin_callback_root(
    callback: CallbackQuery, state: FSMContext
) -> None:
    await del_subadmin_callback(callback, state)


@router.callback_query(F.data == "add_subadmin")
async def add_subadmin_callback_root(
    callback: CallbackQuery, state: FSMContext
) -> None:
    await add_subadmin_callback(callback, state)


@router.callback_query(F.data == "make_mailing")
async def make_mailing_callback_root(
    callback: CallbackQuery, state: FSMContext
) -> None:
    await make_mailing_callback(callback, state)


@router.callback_query(F.data == "ask_del_chat")
async def ask_del_chat_callback_root(
    callback: CallbackQuery, state: FSMContext
) -> None:
    await ask_del_chat_callback(callback, state)


@router.callback_query(F.data == "del_chat")
async def del_chat_callback_root(callback: CallbackQuery, state: FSMContext) -> None:
    await del_chat_callback(callback, state)


@router.callback_query(F.data == "show_confirms")
async def show_confirms_callback_root(
    callback: CallbackQuery, state: FSMContext
) -> None:
    await show_confirms_callback(callback, state)


@router.callback_query(F.data.startswith("show_confirm_"))
async def del_confirm_callback_root(callback: CallbackQuery, state: FSMContext) -> None:
    await del_confirm_callback(callback, state)


@router.callback_query(F.data == "add_confirm")
async def add_confirm_callback_root(callback: CallbackQuery, state: FSMContext) -> None:
    await add_confirm_callback(callback, state)


@router.callback_query(F.data.startswith("end_confirm_"))
async def del_confirm_callback_root(callback: CallbackQuery, state: FSMContext) -> None:
    await del_confirm_callback(callback, state)


@router.callback_query(F.data == "show_chat")
async def show_chat_callback_root(
    callback: CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    await show_chat_callback(callback, bot, state)


@router.callback_query(F.data == "edit_about_quiz")
async def edit_quiz_callback_root(callback: CallbackQuery, state: FSMContext) -> None:
    await edit_quiz_callback(callback, state)


@router.callback_query(F.data == "edit_faq")
async def edit_faq_callback_root(callback: CallbackQuery, state: FSMContext) -> None:
    await edit_faq_callback(callback, state)


@router.callback_query(F.data == "edit_rules")
async def edit_rules_callback_root(callback: CallbackQuery, state: FSMContext) -> None:
    await edit_rules_callback(callback, state)


@router.callback_query(F.data == "show_quizzes")
async def show_quizzes_callback_root(
    callback: CallbackQuery, state: FSMContext
) -> None:
    await show_quizzes_callback(callback, state)


@router.callback_query(F.data.startswith("show_quiz_"))
async def show_quiz_callback_root(callback: CallbackQuery, state: FSMContext) -> None:
    await show_quiz_callback(callback, state)


@router.callback_query(F.data.startswith("edit_quiz_"))
async def edit_quiz_callback_root(callback: CallbackQuery, state: FSMContext) -> None:
    await edit_quiz_callback(callback, state)


@router.callback_query(F.data.startswith("del_quiz_"))
async def del_quiz_callback_root(callback: CallbackQuery, state: FSMContext) -> None:
    await del_quiz_callback(callback, state)


@router.callback_query(F.data == "add_quiz")
async def add_quiz_callback_root(callback: CallbackQuery, state: FSMContext) -> None:
    await add_quiz_callback(callback, state)


@router.callback_query(F.data == "show_all_news")
async def show_all_news_callback_root(
    callback: CallbackQuery, state: FSMContext
) -> None:
    await show_all_news_callback(callback, state)


@router.callback_query(F.data.startswith("show_one_news_"))
async def show_one_news_callback_root(
    callback: CallbackQuery, state: FSMContext
) -> None:
    await show_one_news_callback(callback, state)


@router.callback_query(F.data == "add_news")
async def add_news_callback_root(callback: CallbackQuery, state: FSMContext) -> None:
    await add_news_callback(callback, state)


@router.callback_query(F.data.startswith("edit_news_"))
async def edit_news_callback_root(callback: CallbackQuery, state: FSMContext) -> None:
    await edit_news_callback(callback, state)


@router.callback_query(F.data.startswith("del_news_"))
async def del_news_callback_root(callback: CallbackQuery, state: FSMContext) -> None:
    await del_news_callback(callback, state)


@router.callback_query(F.data == "start")
async def start_callback_root(callback: CallbackQuery, state: FSMContext) -> None:
    await start_callback(callback, state, is_subadmin=False)
