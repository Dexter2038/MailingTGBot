from typing import List, Tuple
from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from app.filters.admin import IsAdminCallback

from app.utils.info import (
    get_about_quiz,
    get_faq,
    get_news_admin,
    get_news_one,
    get_quizzes_admin,
    del_quiz,
    get_quiz,
    del_news,
)
from app.utils.ranks import del_moder, get_moder, get_moders, reset_chat, get_chat_link
from app.database.actions import get_all_confirms, get_confirm, end_confirm

from app.states.admin import Admin

from app.keyboards.admin import (
    get_about_quiz_kb,
    get_add_confirm_kb,
    get_add_moder_kb,
    get_add_news_kb,
    get_add_quiz_kb,
    get_admin_kb,
    get_chat_kb,
    get_confirm_kb,
    get_del_chat_kb,
    get_del_moder_kb,
    get_del_news_kb,
    get_del_quiz_kb,
    get_edit_news_kb,
    get_edit_quiz_kb,
    get_end_confirm_kb,
    get_faq_kb,
    get_mailing_kb,
    get_moders_kb,
    get_moder_kb,
    get_confirms_kb,
    get_news_kb,
    get_news_one_kb,
    get_quiz_kb,
    get_quizzes_kb,
)

router = Router(name="admin_callbacks")

router.callback_query.filter(IsAdminCallback())


@router.callback_query(F.data == "show_moders")
async def show_moders_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    moders = await get_moders()

    if not moders:
        await callback.message.edit_text(
            "Нет модераторов", reply_markup=get_moders_kb()
        )
        return

    text = "Модераторы:\n\n"
    text += "\n".join([f"ID: {moder[0]} - @{moder[1]}" for moder in moders])
    await callback.message.edit_text(
        text, reply_markup=get_moders_kb([moder[0] for moder in moders])
    )


@router.callback_query(F.data.startswith("moder_"))
async def show_moder_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    _, id = callback.data.split("_")

    moder = await get_moder(id)
    if not moder:
        await callback.message.edit_text(
            "Модератор не найден", reply_markup=get_moder_kb(id)
        )
        return

    id, username = moder
    await callback.message.answer(
        f"Модератор:\n\nID: {id}\n@{username}\n\nВыберите действие:",
        reply_markup=get_moder_kb(id),
    )


@router.callback_query(F.data.startswith("del_moder_"))
async def del_moder_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    _, _, id = callback.data.split("_")

    try:
        if await del_moder(id):
            await callback.message.edit_text(
                "Модератор удален", reply_markup=get_del_moder_kb()
            )
        else:
            await callback.message.edit_text(
                "Пользователь не модератор", reply_markup=get_del_moder_kb()
            )

    except Exception:
        await callback.message.edit_text(
            "Произошла ошибка", reply_markup=get_del_moder_kb()
        )


@router.callback_query(F.data == "add_moderator")
async def add_moderator_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Admin.add_moderator)
    await callback.message.edit_text(
        "Отправьте ID и имя пользователя в формате <id> <username> \n\nПример: 1234567890 @username или 1234567890 username",
        reply_markup=get_add_moder_kb(),
    )


@router.callback_query(F.data == "make_mailing")
async def make_mailing_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Admin.make_mailing)
    await callback.message.edit_text(
        "Отправьте текст для рассылки",
        reply_markup=get_mailing_kb(),
    )


@router.callback_query(F.data == "ask_del_chat")
async def ask_del_chat_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.answer(
        "Вы уверены, что хотите сбросить чат вопросов?",
        reply_markup=get_del_chat_kb(True),
    )


@router.callback_query(F.data == "del_chat")
async def del_chat_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    result = await reset_chat()

    if result:
        await callback.message.answer(
            "Чат сброшен.", reply_markup=get_del_chat_kb(False)
        )
    else:
        await callback.message.answer(
            "Чат не сброшен. Произошла ошибка", reply_markup=get_del_chat_kb(False)
        )


@router.callback_query(F.data == "show_confirms")
async def show_confirms_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    confirms = get_all_confirms()

    if not confirms:
        await callback.message.edit_text(
            text="Нет рассылок с подтверждением", reply_markup=get_confirms_kb()
        )
        return

    text = "Рассылки с подтверждением:\n\n"
    text += "\n".join(f"ID: {id} - {text}" for id, text in confirms)

    await callback.message.edit_text(
        text, reply_markup=get_confirms_kb([id for id, _ in confirms])
    )


@router.callback_query(F.data.startswith("show_confirm_"))
async def del_confirm_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    _, _, id = callback.data.split("_")

    data: Tuple[str, List[Tuple[str | int, str]]] = get_confirm(id)

    if not data:
        await callback.message.edit_text(
            "Рассылка с подтверждением не найдена", reply_markup=get_confirm_kb()
        )
        return

    text, users = data

    text: str
    users: List[Tuple[str | int, str]]

    await callback.message.edit_text(
        f"Рассылка с подтверждением:\n\n{text}\n\nПользователи:\n\n{users}\n.Выберите действие:",
        reply_markup=get_confirm_kb(id),
    )


@router.callback_query(F.data == "add_confirm")
async def add_confirm_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Admin.add_confirm)
    await callback.message.edit_text(
        "Отправьте текст для рассылки с подтверждением",
        reply_markup=get_add_confirm_kb(),
    )


@router.callback_query(F.data.startswith("end_confirm_"))
async def del_confirm_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    _, _, id = callback.data.split("_")

    try:
        if end_confirm(id):
            await callback.message.edit_text(
                "Рассылка с подтверждением удалена",
                reply_markup=get_end_confirm_kb(),
            )
        else:
            await callback.message.edit_text(
                "Рассылка с подтверждением не удалена",
                reply_markup=get_end_confirm_kb(),
            )

    except Exception:
        await callback.message.edit_text(
            "Произошла ошибка",
            reply_markup=get_end_confirm_kb(),
        )


@router.callback_query(F.data == "show_chat")
async def show_chat_callback(
    callback: CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    await state.clear()
    chat_link = await get_chat_link(bot)

    if not chat_link:
        await callback.message.edit_text(
            "Чат не инициализирован",
            reply_markup=get_chat_kb(None),
        )
        return

    await callback.message.edit_text(
        f"Ссылка на чат: {chat_link}",
        reply_markup=get_chat_kb(chat_link),
    )


@router.callback_query(F.data == "edit_about_quiz")
async def edit_quiz_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Admin.edit_about_quiz)
    about_quiz = await get_about_quiz()

    if not about_quiz:
        await callback.message.edit_text(
            "Отправьте текст для выставления в О викторине",
            reply_markup=get_about_quiz_kb(),
        )
        return

    await callback.message.edit_text(
        f"О викторине:\n{about_quiz}\n\n"
        "Отправьте текст для выставления в О викторине",
        reply_markup=get_about_quiz_kb(),
    )


@router.callback_query(F.data == "edit_faq")
async def edit_faq_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Admin.edit_faq)
    faq = await get_faq()

    if not faq:
        await callback.message.edit_text(
            "Отправьте текст для выставления в Частые вопросы",
            reply_markup=get_faq_kb(),
        )

    await callback.message.edit_text(
        f"Частые вопросы:\n{faq}\n\n"
        "Отправьте текст для выставления в Частые вопросы",
        reply_markup=get_faq_kb(),
    )


@router.callback_query(F.data == "show_quizzes")
async def show_quizzes_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    quizzes = await get_quizzes_admin()

    if not quizzes:
        await callback.message.edit_text(
            "Нет викторин",
            reply_markup=get_quizzes_kb(),
        )
        return

    text = "Викторины:\n\n"
    text += "\n".join(f"ID: {quiz[0]} - {quiz[1]}" for quiz in quizzes)

    await callback.message.edit_text(
        text, reply_markup=get_quizzes_kb([quiz[0] for quiz in quizzes])
    )


@router.callback_query(F.data.startswith("show_quiz_"))
async def show_quiz_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    _, _, id = callback.data.split("_")

    quiz = await get_quiz(id)

    if not quiz:
        await callback.message.edit_text(
            "Викторина не найдена",
            reply_markup=get_quiz_kb(),
        )
        return

    await callback.message.edit_text(
        f"Викторина:\n\n{quiz}\n\nВыберите действие:",
        reply_markup=get_quiz_kb(id),
    )


@router.callback_query(F.data.startswith("edit_quiz_"))
async def edit_quiz_callback(callback: CallbackQuery, state: FSMContext) -> None:
    _, _, id = callback.data.split("_")
    await state.set_state(Admin.edit_quiz)
    await callback.message.edit_text(
        "Отправьте текст для редактирования предстоящей викторины",
        reply_markup=get_edit_quiz_kb(id),
    )

    await state.update_data(id=id)


@router.callback_query(F.data.startswith("del_quiz_"))
async def del_quiz_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    _, _, id = callback.data.split("_")

    if await del_quiz(id):
        await callback.message.edit_text(
            "Викторина удалена",
            reply_markup=get_del_quiz_kb(),
        )
    else:
        await callback.message.edit_text(
            "Викторина не удалена",
            reply_markup=get_del_quiz_kb(),
        )


@router.callback_query(F.data == "add_quiz")
async def add_quiz_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Admin.add_quiz)
    await callback.message.edit_text(
        "Отправьте текст для добавления викторины",
        reply_markup=get_add_quiz_kb(),
    )


@router.callback_query(F.data == "show_all_news")
async def show_all_news_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    news = await get_news_admin()

    if not news:
        await callback.message.edit_text(
            "Нет новостей",
            reply_markup=get_news_kb(),
        )
        return

    text = "Новости:\n\n"
    text += "\n".join(f"ID: {news[0]} - {news[1]}" for news in news)

    await callback.message.edit_text(
        text, reply_markup=get_news_kb([news[0] for news in news])
    )


@router.callback_query(F.data.startswith("show_one_news_"))
async def show_one_news_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    _, _, _, id = callback.data.split("_")

    news = await get_news_one(int(id))

    if not news:
        await callback.message.edit_text(
            "Новость не найдена",
            reply_markup=get_news_kb(),
        )
        return

    id, description = news

    await callback.message.edit_text(
        f"Новость:\n\nID:{id} - {description}\n\nВыберите действие:",
        reply_markup=get_news_one_kb(id),
    )


@router.callback_query(F.data == "add_news")
async def add_news_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Admin.add_news)
    await callback.message.edit_text(
        "Отправьте текст для добавления новости",
        reply_markup=get_add_news_kb(),
    )


@router.callback_query(F.data.startswith("edit_news_"))
async def edit_news_callback(callback: CallbackQuery, state: FSMContext) -> None:
    _, _, id = callback.data.split("_")
    await state.set_state(Admin.edit_news)
    await callback.message.edit_text(
        "Отправьте текст для редактирования предстоящей новости",
        reply_markup=get_edit_news_kb(id),
    )

    await state.update_data(id=id)


@router.callback_query(F.data.startswith("del_news_"))
async def del_news_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    _, _, id = callback.data.split("_")
    if await del_news(id):
        await callback.message.edit_text(
            "Новость удалена",
            reply_markup=get_del_news_kb(),
        )
    else:
        await callback.message.edit_text(
            "Новость не удалена",
            reply_markup=get_del_news_kb(),
        )


@router.callback_query(F.data == "start")
async def start_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text(
        "Здравствуйте!\nВыберите действие",
        reply_markup=get_admin_kb(),
    )
