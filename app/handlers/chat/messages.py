from aiogram import F, Bot, Router
from aiogram.types import Message
from aiogram.filters import Command

from app.filters.chat import IsChatMessage
from app.utils.ranks import get_chat_id, is_able_to_answer, set_chat_id

router = Router(name="chat_messages")


@router.message(F.reply_to_message.from_user.is_bot, IsChatMessage())
async def answer_to_message(message: Message, bot: Bot):
    """
    Обрабатывает ответы на вопросы в чате.

    :param message: Объект Message, представляющий сообщение.
    :param bot: Объект Bot, представляющий бота, который отправляет сообщение.
    :return: None

    Внутренний процесс:
    1. Получаем ID чата и ID сообщения, на которое отвечает пользователь.
    2. Если пользователь не является модератором или администратором, удаляем его сообщение.
    3. Отправляем ответ модератора пользователю в чат.
    4. Удаляем ответ модератора.
    """

    try:
        data = message.reply_to_message.text.split("]", maxsplit=1)[0]
        data = data.split("[", maxsplit=1)[1]
        chat_id, msg_id = data.split(", ")
        if not await is_able_to_answer(message.from_user.id):
            await message.delete()
            return

        answer_text = f"{message.text}\n\nНа ваш вопрос ответила команда escape!"

        await bot.send_message(chat_id, answer_text, reply_to_message_id=msg_id)

        await message.reply_to_message.delete()
        await message.delete()
        print("Дошёл")
    except Exception as e:
        print(e)
        return  # ничего не делать


@router.message(Command("initchat"), F.chat.type == "group")
@router.message(Command("initchat"), F.chat.type == "supergroup")
async def init_chat_command(message: Message) -> None:
    if await get_chat_id():
        return

    await message.chat.create_invite_link()

    await set_chat_id(message.chat.id)
    await message.answer("Чат успешно инициализирован!")
