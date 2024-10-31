from typing import List, Tuple
from aiogram import Bot, Router
from aiogram.filters import Command, CommandObject, and_f
from aiogram.types import Message

from app.database.actions import end_confirm, get_all_confirms, get_confirm_users
from app.filters.admin import IsAdmin
from app.utils.mail import send_confirm_mailing, send_mailing
from app.utils.moders import get_moders, add_moder, del_moder


router = Router(name=__name__)


@router.message(and_f(Command("moders"), IsAdmin()))
async def admins(message: Message) -> None:
    moders: List[Tuple[str, str]] = get_moders()

    result = "\n".join(" ".join(sublist) for sublist in moders)

    await message.answer(
        text=(
            """
        Список модераторов:\n%s
    """
            % result
        )
    )


@router.message(and_f(Command("addmoder"), IsAdmin()))
async def addmoder(message: Message, command: CommandObject) -> None:
    arg: List[str] = command.args.split(sep=" ")

    if len(arg) != 2 or not arg[0].isdigit() or not arg[1].isdigit():
        await message.answer(text="Формат /addmoder <id> <username>")
        return

    id, username = arg

    add_moder(id, username)

    await message.answer(text="Добавлен модератор %s" % username)


@router.message(and_f(Command("delmoder"), IsAdmin()))
async def delmoder(message: Message, command: CommandObject) -> None:
    arg: List[str] = command.args.split(sep=" ")

    if len(arg) != 1 or not arg[0].isdigit():
        await message.answer(
            text=f"Неверное количество аргументов. Формат: /delmoder <id/username>"
        )
        return

    moder: str = arg[0]

    del_moder(moder)

    await message.answer(text="Удален модератор %s" % moder)


@router.message(and_f(Command("mailing"), IsAdmin()))
async def mailing(message: Message, command: CommandObject, bot: Bot) -> None:
    text: str = command.args

    if not text:
        await message.answer(text="Формат: '/mailing текст'")
        return

    await send_mailing(text, bot)

    await message.answer(text="Отправлено!")


@router.message(and_f(Command("delchat"), IsAdmin()))
async def delchat(message: Message) -> None:
    with open(file="chat.txt", mode="w") as f:
        f.write("")
    await message.answer(text="Чат аннулирован")


@router.message(and_f(Command("addconfirm"), IsAdmin()))
async def addconfirm(message: Message, command: CommandObject) -> None:
    args = command.args

    if args == "":
        await message.answer(text="Формат: /addconfirm <текст>")
        return

    send_confirm_mailing(text=args)

    await message.answer(text="Рассылка с подтверждением добавлена")


@router.message(and_f(Command("confirms"), IsAdmin()))
async def confirms(message: Message) -> None:
    confirms_list: List[Tuple[int, str]] = get_all_confirms()

    if not confirms_list:
        await message.answer(text="Нет рассылок с подтверждением")
        return

    for id, text in confirms_list:
        await message.answer(text=f"{id} - {text}")


@router.message(and_f(Command("confirm"), IsAdmin()))
async def confirm_users(message: Message, command: CommandObject) -> None:
    args: List[str] = command.args.split(" ")

    if args > 1 or not args[0].isdigit():
        await message.answer(text="Формат: /confirm <id конкурса с подтверждением>")
        return

    info: List[Tuple[int | str]] = get_confirm_users(id=args[0])

    if not info:
        await message.answer(text="Нет подтвержденных пользователей")
        return

    text = "\n".join([f"ID: {id} - Nickname{name}" for id, name in info])

    await message.answer(text=text)


@router.message(and_f(Command("delconfirm"), IsAdmin()))
async def delconfirm(message: Message, command: CommandObject) -> None:
    args: List[str] = command.args.split(" ")

    if args > 1 or not args[0].isdigit():
        await message.answer(text="Формат: /delconfirm <id конкурса с подтверждением>")
        return

    if end_confirm(id=args[0]):
        await message.answer(text="Конкурс с подтверждением закончен")
    else:
        await message.answer(text="Не получилось закончить конкурс с подтверждением")
