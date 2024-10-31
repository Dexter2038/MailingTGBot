from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_help_kb() -> InlineKeyboardMarkup:
    """
    Возвращает готовую клавиатуру с переключением на:

    Список функций бота

    FAQ (Частые вопросы)

    Возможность задать вопрос

    :param: None
    :return: InlineKeyboardMarkup
    """

    kb = InlineKeyboardBuilder()

    kb.add(
        InlineKeyboardButton(text="Функции бота", callback_data="BotFunctions"),
        InlineKeyboardButton(text="FAQ (Частые вопросы)", callback_data="FAQ"),
        InlineKeyboardButton(text="Задать вопрос", callback_data="AskQuestion"),
    )

    # Регулирование расположения кнопок
    # kb.adjust()

    return kb.as_markup()


def get_ask_help_kb() -> InlineKeyboardMarkup:
    """
    Возвращает готовую клавиатуру с возможностями:

    Перейти в режим задания вопроса

    Воздержаться

    :param: None
    :return: InlineKeyboardMarkup
    """

    kb = InlineKeyboardBuilder()

    kb.add(
        InlineKeyboardButton(text="Да", callback_data="AskQuestionYes"),
        InlineKeyboardButton(text="Нет", callback_data="AskQuestionNo"),
    )

    # Регулирование расположения кнопок
    # kb.adjust()

    return kb.as_markup()


def get_question_kb(chat_id: int, msg_id: int) -> InlineKeyboardMarkup:
    """
    Возвращает готовую клавиатуру с возможностями:

    Взять на себя вопрос

    Отклонить вопрос

    Args:
        chat_id: int - id чата пользователя
        msg_id: int - id сообщения пользователя

    Returns:
        InlineKeyboardMarkup
    """

    kb = InlineKeyboardBuilder()

    kb.add(
        InlineKeyboardButton(
            text="Взять на себя вопрос",
            callback_data=f"TakeQuestion_{chat_id}_{msg_id}",
        ),
        InlineKeyboardButton(
            text="Отклонить вопрос", callback_data=f"DeclineQuestion_{chat_id}_{msg_id}"
        ),
    )

    # Регулирование расположения кнопок
    # kb.adjust()

    return kb.as_markup()
