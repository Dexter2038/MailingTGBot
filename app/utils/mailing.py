from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup


from app.database.actions import add_confirm, get_all_ids
from app.keyboards.user import get_confirm_mailing_kb


async def make_mailing(text: str, bot: Bot) -> bool:
    """
    Отправляет сообщение с текстом text
    всем зарегистрированным пользователям.

    Args:
        text (str): текст сообщения.
        bot (Bot): объект бота, который отправляет сообщение.

    Returns:
        bool: флаг успешности отправки.
    """
    try:
        ids = get_all_ids()

        for id in ids:
            await bot.send_message(id, text)

        return True

    except Exception as e:
        print(e)
        print("Не получилось отправить сообщение всем пользователям")
        return False


async def make_confirm_mailing(text: str, bot: Bot) -> bool:
    """
    Отправляет сообщение с текстом text
    всем зарегистрированным пользователям.

    Args:
        text (str): текст сообщения.
        bot (Bot): объект бота, который отправляет сообщение.

    Returns:
        bool: флаг успешности отправки.
    """
    try:
        ids = get_all_ids()

        mailing_id: int = add_confirm(text)

        kb: InlineKeyboardMarkup = get_confirm_mailing_kb(mailing_id)

        for id in ids:
            await bot.send_message(id, text, reply_markup=kb)

        return True

    except Exception as e:
        print(e)
        print("Не получилось отправить сообщение всем пользователям")
        return False
