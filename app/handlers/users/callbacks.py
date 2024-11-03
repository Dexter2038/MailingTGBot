from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from app.keyboards.user import get_user_kb, get_back_kb
from app.utils.info import get_about_quiz, get_faq, get_news_user, get_quizzes_user
from app.states.user import User


router = Router(name="user_callbacks")


@router.callback_query(F.data == "start")
async def start_callback(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        "Здравствуйте!\nВыберите действие", reply_markup=get_user_kb()
    )


@router.callback_query(F.data == "about_quiz")
async def about_quiz_callback(callback: CallbackQuery) -> None:
    about_quiz = await get_about_quiz()

    if not about_quiz:
        await callback.message.edit_text(
            "Информация о викторине не найдена", reply_markup=get_back_kb()
        )
        return

    await callback.message.edit_text(
        f"О викторине:\n\n{about_quiz}", reply_markup=get_back_kb()
    )


@router.callback_query(F.data == "faq")
async def faq_callback(callback: CallbackQuery) -> None:
    faq = await get_faq()

    if not faq:
        await callback.message.edit_text(
            "Информация о частых вопросах не найдена", reply_markup=get_back_kb()
        )
        return

    await callback.message.edit_text(
        f"Частые вопросы:\n\n{faq}", reply_markup=get_back_kb()
    )


@router.callback_query(F.data == "quizzes")
async def quizzes_callback(callback: CallbackQuery) -> None:
    quizzes = await get_quizzes_user()

    if not quizzes:
        await callback.message.edit_text(
            "Нет предстоящих викторин", reply_markup=get_back_kb()
        )
        return

    text = "Предстоящие викторины:\n\n"
    text += "\n".join(quizzes)

    await callback.message.edit_text(text, reply_markup=get_back_kb())


@router.callback_query(F.data == "news")
async def news_callback(callback: CallbackQuery) -> None:
    news = await get_news_user()

    if not news:
        await callback.message.edit_text("Нет новостей", reply_markup=get_back_kb())
        return

    text = "Новости:\n\n"
    text += "\n".join(news)

    await callback.message.edit_text(text, reply_markup=get_back_kb())


[
    "about_quiz",
    "faq",
    "quizzes",
    "news",
    "change_email",
    "get_id",
    "ask_question",
]


@router.callback_query(F.data == "change_email")
async def change_email_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text(
        "Напишите вашу новую почту", reply_markup=get_back_kb()
    )

    await state.set_state(User.change_email)


@router.callback_query(F.data == "get_id")
async def get_id_callback(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        f"Ваш ID: {callback.from_user.id}", reply_markup=get_back_kb()
    )


@router.callback_query(F.data == "ask_question")
async def ask_question_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.edit_text("Напишите ваш вопрос", reply_markup=get_back_kb())

    await state.set_state(User.ask_question)
