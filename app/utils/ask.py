from aiogram import Bot

from app.keyboards.moder import get_question_kb
from app.utils.ranks import get_chat_id


async def ask_question(
    chat_id: int, msg_id: int, username: str, bot: Bot, text: str
) -> bool:
    """
    Отправляет сообщение в чат поддержки

    Args:
        text (str): текст сообщения.
        bot (Bot): объект бота, который отправляет сообщение.
        chat_id (int): id чата пользователя, который отправляет вопрос
        msg_id (int): id сообщения пользователя, который отправляет вопрос
        username (str): имя пользователя

    Returns:
        bool: флаг успешности отправки.
    """
    chat = await get_chat_id()
    if not chat:
        return False

    await bot.send_message(
        chat,
        f"Вопрос[{chat_id}, {msg_id}]:\nВопрос от {username}:\n{text}",
        reply_markup=get_question_kb(),
    )
    return True
