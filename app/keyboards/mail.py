from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_mail_kb() -> InlineKeyboardMarkup:
    """
    Возвращает готовую клавиатуру с возможностями:

    Да - изменить email

    Нет - не изменять email

    :param: None
    :return: InlineKeyboardMarkup
    """
    kb = InlineKeyboardBuilder()

    kb.add(
        InlineKeyboardButton(text="Да", callback_data="ChangeMailYes"),
        InlineKeyboardButton(text="Нет", callback_data="ChangeMailNo"),
    )

    # Регулирование расположения кнопок
    # kb.adjust()

    return kb.as_markup()

