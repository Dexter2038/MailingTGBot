from typing import List
from aiogram import F, Bot, Router
from aiogram.filters import Command, CommandObject, and_f
from aiogram.types import Message, CallbackQuery

from app.filters.chat import IsChatCallback, IsChatMessage
from app.utils.moders import add_moder, del_moder


router = Router(name=__name__)


@router.message(Command("initchat"))
async def initchat(message: Message, command: CommandObject) -> None:
    with open("chat.txt", "r+") as f:
        res: str = f.read()
        if res != "":
            await message.answer(
                text="Чат уже инициализирован, чтобы аннулировать чат админ должен ввести /delchat"
            )
            return
        f.write(str(message.chat.id))
    await message.answer(text="Чат инициализирован")


@router.callback_query(and_f(F.data.startswith("TakeQuestion_"), IsChatCallback()))
async def take_question(callback: CallbackQuery, bot: Bot) -> None:
    _, chat_id, msg_id = callback.data.split("_")

    await callback.message.edit_text(
        text=callback.message.text
        + "\n\nВопрос взял модератор %s" % callback.from_user.username
    )
    await bot.send_message(
        callback.from_user.id,
        (
            """Вопрос[%s, %s].\n
Вы взялись за вопрос: '%s'.\n
Чтобы ответить на него,
напишите ответное сообщение,
используя функцию 'ответить'
    """
            % (chat_id, msg_id, callback.message.text)
        ),
    )


@router.callback_query(and_f(F.data.startswith("DeclineQuestion_"), IsChatCallback()))
async def decline_question(callback: CallbackQuery, bot: Bot) -> None:
    _, chat_id, msg_id = callback.data.split("_")

    await bot.send_message(chat_id, "Ваш вопрос отклонён", reply_to_message_id=msg_id)

    await callback.message.edit_text(
        text=callback.message.text
        + "\n\nВопрос отклонил модератор %s" % callback.from_user.username
    )


@router.message(and_f(F.new_chat_members, IsChatMessage()))
async def chat_member(message: Message) -> None:
    if add_moder(message.new_chat_members[0].id):
        await message.answer(
            "Добавлен модератор %s" % message.new_chat_members[0].username
        )
    else:
        await message.answer(
            "Добро пожаловать в чат! " + message.new_chat_members[0].username
        )


@router.message(and_f(F.left_chat_member, IsChatMessage()))
async def left_chat_member(message: Message) -> None:
    del_moder(message.left_chat_member.id)
    await message.answer("Модератор %s покинул чат" % message.left_chat_member.username)
