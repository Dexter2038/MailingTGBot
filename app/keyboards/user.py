from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_user_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    kb.add(
        InlineKeyboardButton(text="О викторине", callback_data="about_quiz"),
        InlineKeyboardButton(text="Частые вопросы", callback_data="faq"),
        InlineKeyboardButton(text="Предстоящие викторины", callback_data="quizzes"),
        InlineKeyboardButton(text="Новости", callback_data="news"),
        InlineKeyboardButton(text="Правила", callback_data="rules"),
        InlineKeyboardButton(text="Изменить почту", callback_data="change_email"),
        InlineKeyboardButton(text="Получить свой id", callback_data="get_id"),
        InlineKeyboardButton(text="Задать вопрос", callback_data="ask_question"),
    )

    kb.adjust(1)

    return kb.as_markup()


def get_confirm_mailing_kb(active_id: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(
        InlineKeyboardButton(
            text="Подтвердить участие", callback_data=f"participate_{active_id}"
        )
    )
    kb.row(InlineKeyboardButton(text="Отказаться", callback_data="not_participate"))
    return kb.as_markup()


def get_back_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text="Назад", callback_data="start"))

    return builder.as_markup()
