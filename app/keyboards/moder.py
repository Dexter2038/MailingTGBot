from typing import List, Optional
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_moder_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text="Войти в чат вопросов", callback_data="show_chat")
    )

    return builder.as_markup()


def get_back_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text="Назад", callback_data="start"))

    return builder.as_markup()


def get_chat_kb(chat_link: Optional[str] = "") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if chat_link:
        builder.row(InlineKeyboardButton(text="Ссылка на чат", url=f"{chat_link}"))
    builder.row(InlineKeyboardButton(text="Назад", callback_data="start"))
    return builder.as_markup()


def get_question_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Отклонить вопрос",
            callback_data="decline_question",
        )
    )
    return builder.as_markup()
