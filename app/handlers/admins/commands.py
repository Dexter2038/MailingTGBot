from typing import List, Tuple
from aiogram import Bot, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message


from app.keyboards.admin import get_admin_kb
from app.utils.ranks import get_moders, reset_chat, get_chat_link, add_moder, del_moder
from app.utils.mailing import make_confirm_mailing, make_mailing
from app.utils.info import (
    add_news,
    add_quiz,
    edit_about_quiz,
    get_about_quiz,
    edit_faq,
    get_faq,
    edit_news,
    get_news_admin,
    del_news,
    get_quizzes_admin,
    get_quiz,
    edit_quiz,
    del_quiz,
)

from app.database.actions import end_confirm, get_all_confirms, get_confirm

router = Router(name="admin_messages")


@router.message(Command("start"))
async def start_command(message: Message) -> None:

    await message.answer(
        "Привет, администратор! Команды доступны по команде /commands",
        reply_markup=get_admin_kb(),
    )


@router.message(Command("commands"))
async def commands_command(message: Message) -> None:
    text = (
        "Доступные команды:\n\n"
        "/start - начать работу с ботом\n"
        "/addmoder <id> <username> - назначить пользователя модератором\n"
        "/delmoder <id/username> - убрать пользователя из списка модераторов\n"
        "/moders - посмотреть список модераторов\n"
        "/mailing <текст> - сделать рассылку всем пользователям\n"
        "/confirms - посмотреть список рассылки с подтверждением\n"
        "/confirm <id> - посмотреть участников конкретной рассылки с подтверждением\n"
        "/addconfirm <текст> - начать рассылку с подтверждением\n"
        "/endconfirm <id> - завершить конкретную рассылку с подтверждением\n"
        "/initchat (только в групповом чате) - инициализировать чат с вопросами\n"
        "/askchat - получить ссылку на чат с вопросами\n"
        "/delchat - сбросить чат с вопросами\n"
        "/editaboutquiz <текст> - редактировать информацию о викторине\n"
        "/aboutquiz - посмотреть информацию о викторине\n"
        "/editfaq <текст> - редактировать информацию о частых вопросах\n"
        "/faq - посмотреть информацию о частых вопросах\n"
        "/news - посмотреть новости\n"
        "/editnews <id> <текст> - редактировать новость\n"
        "/delnews <id> - удалить новость\n"
        "/quizzes - посмотреть предстоящие викторины\n"
        "/quiz <id> - посмотреть текст предстоящей викторины\n"
        "/editquiz <id> <текст> - редактировать текст предстоящей викторины\n"
        "/delquiz <id> - удалить информацию о предстоящей викторине\n"
        "/commands - посмотреть доступные команды\n"
    )

    await message.answer(text)


@router.message(Command("moders"))
async def show_moderators_command(message: Message) -> None:
    moders = await get_moders()
    if not moders:
        await message.answer("Нет модераторов")
        return

    text = "Модераторы:\n\n"
    text += "\n".join([f"ID: {moder[0]} - @{moder[1]}" for moder in moders])
    await message.answer(text)


@router.message(Command("addmoder"))
async def add_moderator_command(message: Message, command: CommandObject) -> None:
    args = command.args
    try:
        args = args.split(" ")
    except Exception:
        await message.answer(
            "Неверный формат команды. Используйте /addmoder <id> <username>. Пример: 123 @username или 123 username"
        )
        return

    if len(args) != 2 or not args[0].isdigit():
        await message.answer(
            "Неверный формат команды. Используйте /addmoder <id> <username>. Пример: 123 @username или 123 username"
        )
        return

    id, username = args

    username = username.replace("@", "")

    try:
        result = await add_moder(id, username)

        if result:
            await message.answer("Пользователь назначен модератором")
        else:
            await message.answer("Пользователь уже модератор")

    except Exception as e:
        await message.answer("Пользователь не назначен модератором. Произошла ошибка")


@router.message(Command("delmoder"))
async def del_moderator_command(message: Message, command: CommandObject) -> None:
    args = command.args
    try:
        args = args.split(" ")
    except AttributeError:
        await message.answer(
            "Неверный формат команды. Используйте /delmoder <id/username>"
        )
        return

    if len(args) != 1:
        await message.answer(
            "Неверный формат команды. Используйте /delmoder <id/username>"
        )
        return

    id = args[0]

    try:
        result = await del_moder(id)

        if result:
            await message.answer("Пользователь удален из списка модераторов")
        else:
            await message.answer("Пользователь не модератор")

    except Exception as e:
        await message.answer(
            "Пользователь не удален из списка модераторов. Произошла ошибка"
        )


@router.message(Command("mailing"))
async def send_mailing_command(
    message: Message, command: CommandObject, bot: Bot
) -> None:
    text = command.args
    if not text:
        await message.answer("Неверный формат команды. Используйте /mailing <текст>")
        return

    result = await make_mailing(text, bot)

    if result:
        await message.answer("Рассылка выполнена")
    else:
        await message.answer("Рассылка не выполнена. Произошла ошибка")


@router.message(Command("delchat"))
async def del_chat_command(message: Message) -> None:
    result = await reset_chat()

    if result:
        await message.answer("Чат сброшен")
    else:
        await message.answer("Чат не сброшен. Произошла ошибка")


@router.message(Command("confirms"))
async def show_confirms_command(message: Message) -> None:
    confirms = get_all_confirms()
    if not confirms:
        await message.answer("Нет рассылок с подтверждением")
        return

    text = "Рассылки с подтверждением:\n\n"
    text += "\n".join(f"ID: {id} - {text}" for id, text in confirms)

    await message.answer(text)


@router.message(Command("confirm"))
async def show_confirm_command(message: Message, command: CommandObject) -> None:
    args = command.args
    try:
        args = args.split(" ")
    except AttributeError:
        await message.answer("Неверный формат команды. Используйте /confirm <id>")
        return

    if len(args) != 1 or not args[0].isdigit():
        await message.answer("Неверный формат команды. Используйте /confirm <id>")
        return

    id = args[0]

    confirm = get_confirm(id)

    if not confirm:
        await message.answer("Рассылка с подтверждением не найдена")
        return
    description, users = confirm

    description: str
    Users: List[Tuple[int, str]]

    text = (
        f"Рассылка с подтверждением:\n\n"
        f"ID: {id}\n"
        f"Текст: {description}\nУчастники:\n"
    )
    text += "\n".join(f"ID: {id} - @{username}" for id, username in users)

    await message.answer(text)


@router.message(Command("addconfirm"))
async def add_confirm_command(
    message: Message, command: CommandObject, bot: Bot
) -> None:
    text = command.args

    if not text:
        await message.answer("Неверный формат команды. Используйте /addconfirm <текст>")
        return

    result = await make_confirm_mailing(text, bot)

    if result:
        await message.answer("Рассылка с подтверждением выполнена")
    else:
        await message.answer("Рассылка с подтверждением не выполнена. Произошла ошибка")


@router.message(Command("endconfirm"))
async def del_confirm_command(message: Message, command: CommandObject) -> None:
    args = command.args
    try:
        args = args.split(" ")
    except AttributeError:
        await message.answer("Неверный формат команды. Используйте /endconfirm <id>")
        return

    if len(args) != 1:
        await message.answer("Неверный формат команды. Используйте /endconfirm <id>")
        return

    id = args[0]

    result = end_confirm(id)

    if result:
        await message.answer("Рассылка с подтверждением закончена")
    else:
        await message.answer("Рассылка с подтверждением не закончена. Произошла ошибка")


@router.message(Command("askchat"))
async def show_chat_command(message: Message, bot: Bot) -> None:
    chat_link = await get_chat_link(bot)

    if not chat_link:
        await message.answer("Чат не инициализирован")
        return

    await message.answer(f"Ссылка на чат: {chat_link}")


@router.message(Command("editaboutquiz"))
async def edit_about_quiz_command(message: Message, command: CommandObject) -> None:
    args = command.args

    if not args:
        await message.answer(
            "Неверный формат команды. Используйте /editaboutquiz <текст>"
        )
        return

    result = await edit_about_quiz(args)

    if result:
        await message.answer("Информация о викторине обновлена")
    else:
        await message.answer("Информация о викторине не обновлена. Произошла ошибка")


@router.message(Command("aboutquiz"))
async def show_about_quiz_command(message: Message) -> None:
    quiz_info = await get_about_quiz()

    if not quiz_info:
        await message.answer("Информация о викторине не найдена")
        return

    await message.answer(quiz_info)


@router.message(Command("editfaq"))
async def edit_faq_command(message: Message, command: CommandObject) -> None:
    args = command.args

    if not args:
        await message.answer("Неверный формат команды. Используйте /editfaq <текст>")
        return

    result = await edit_faq(args)

    if result:
        await message.answer("Информация о частых вопросах обновлена")
    else:
        await message.answer(
            "Информация о частых вопросах не обновлена. Произошла ошибка"
        )


@router.message(Command("faq"))
async def show_faq_command(message: Message) -> None:
    faq = await get_faq()

    if not faq:
        await message.answer("Информация о частых вопросах не найдена")
        return

    await message.answer(faq)


@router.message(Command("news"))
async def show_news_command(message: Message) -> None:
    news = await get_news_admin()

    if not news:
        await message.answer("Новости не найдены")
        return

    text = "Новости:\n\n"
    text += "\n".join(f"ID: {new[0]} - {new[1]}" for new in news)

    await message.answer(text)


@router.message(Command("addnews"))
async def add_news_command(message: Message, command: CommandObject) -> None:
    args = command.args

    if not args:
        await message.answer("Неверный формат команды. Используйте /addnews <текст>")
        return

    result = await add_news(args)

    if result:
        await message.answer("Новость добавлена")
    else:
        await message.answer("Новость не добавлена. Произошла ошибка")


@router.message(Command("editnews"))
async def edit_news_command(message: Message, command: CommandObject) -> None:
    args = command.args
    try:
        args = args.split(" ")
    except AttributeError:
        await message.answer(
            "Неверный формат команды. Используйте /editnews <id> <текст>"
        )
        return

    if len(args) < 2 or not args[0].isdigit():
        await message.answer(
            "Неверный формат команды. Используйте /editnews <id> <текст>"
        )
        return

    id = args[0]
    text = " ".join(args[1:])

    result = await edit_news(id, text)

    if result:
        await message.answer("Новость обновлена")
    else:
        await message.answer("Новость не обновлена. Произошла ошибка")


@router.message(Command("delnews"))
async def delete_news_command(message: Message, command: CommandObject) -> None:
    args = command.args
    try:
        args = args.split(" ")
    except AttributeError:
        await message.answer("Неверный формат команды. Используйте /delnews <id>")
        return

    if len(args) != 1:
        await message.answer("Неверный формат команды. Используйте /delnews <id>")
        return

    id = args[0]

    result = await del_news(id)

    if result:
        await message.answer("Новость удалена")
    else:
        await message.answer("Новость не удалена. Произошла ошибка")


@router.message(Command("quizzes"))
async def show_quizzes_command(message: Message) -> None:
    quizzes = await get_quizzes_admin()

    if not quizzes:
        await message.answer("Предстоящие викторины не найдены")
        return

    text = "Предстоящие викторины:\n\n"
    text += "\n".join(f"ID: {quiz[0]} - {quiz[1]}" for quiz in quizzes)

    await message.answer(text)


@router.message(Command("quiz"))
async def show_quiz_command(message: Message, command: CommandObject) -> None:
    args = command.args
    try:
        args = args.split(" ")
    except AttributeError:
        await message.answer("Неверный формат команды. Используйте /quiz <id>")
        return

    if len(args) != 1:
        await message.answer("Неверный формат команды. Используйте /quiz <id>")
        return

    id = args[0]

    quiz = await get_quiz(id)

    if not quiz:
        await message.answer("Предстоящая викторина не найдена")
        return

    await message.answer(quiz)


@router.message(Command("addquiz"))
async def add_quiz_command(message: Message, command: CommandObject) -> None:
    args = command.args

    if not args:
        await message.answer("Неверный формат команды. Используйте /addquiz <текст>")
        return

    result = await add_quiz(args)

    if result:
        await message.answer("Предстоящая викторина добавлена")
    else:
        await message.answer("Предстоящая викторина не добавлена. Произошла ошибка")


@router.message(Command("editquiz"))
async def edit_quiz_command(message: Message, command: CommandObject) -> None:
    args = command.args
    try:
        args = args.split(" ")
    except AttributeError:
        await message.answer(
            "Неверный формат команды. Используйте /editquiz <id> <текст>"
        )
        return

    if len(args) < 2 or not args[0].isdigit():
        await message.answer(
            "Неверный формат команды. Используйте /editquiz <id> <текст>"
        )
        return

    id = args[0]
    text = " ".join(args[1:])

    result = await edit_quiz(id, text)

    if result:
        await message.answer("Предстоящая викторина обновлена")
    else:
        await message.answer("Предстоящая викторина не обновлена. Произошла ошибка")


@router.message(Command("delquiz"))
async def delete_quiz_command(message: Message, command: CommandObject) -> None:
    args = command.args
    try:
        args = args.split(" ")
    except AttributeError:
        await message.answer("Неверный формат команды. Используйте /delquiz <id>")
        return

    if len(args) != 1:
        await message.answer("Неверный формат команды. Используйте /delquiz <id>")
        return

    id = args[0]

    result = await del_quiz(id)

    if result:
        await message.answer("Предстоящая викторина удалена")
    else:
        await message.answer("Предстоящая викторина не удалена. Произошла ошибка")


@router.message(Command("addquiz"))
async def add_quiz_command(message: Message, command: CommandObject) -> None:
    text = command.args

    if not text:
        await message.answer("Неверный формат команды. Используйте /addquiz <текст>")
        return

    result = await add_quiz(text)

    if result:
        await message.answer("Предстоящая викторина добавлена")
    else:
        await message.answer("Предстоящая викторина не добавлена. Произошла ошибка")


@router.message()
async def echo_message(message: Message) -> None:
    return
