from aiogram import Bot, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from app.handlers.functions.admin.commands import *


router = Router(name="root_messages")


@router.message(Command("start"))
async def start_command_root(message: Message) -> None:
    await start_command(message, is_subadmin=False)


@router.message(Command("commands"))
async def commands_command_root(message: Message) -> None:
    await commands_command(message, is_subadmin=False)


@router.message(Command("moders"))
async def show_moderators_command_root(message: Message) -> None:
    await show_moderators_command(message)


@router.message(Command("addmoder"))
async def add_moderator_command_root(message: Message, command: CommandObject) -> None:
    await add_moderator_command(message, command)


@router.message(Command("delmoder"))
async def del_moderator_command_root(message: Message, command: CommandObject) -> None:
    await del_moderator_command(message, command)


@router.message(Command("subadmins"))
async def show_subadmins_command_root(message: Message) -> None:
    await show_subadmins_command(message)


@router.message(Command("addsubadmin"))
async def add_subadmin_command_root(message: Message, command: CommandObject) -> None:
    await add_subadmin_command(message, command)


@router.message(Command("delsubadmin"))
async def del_subadmin_command_root(message: Message, command: CommandObject) -> None:
    await del_subadmin_command(message, command)


@router.message(Command("mailing"))
async def send_mailing_command_root(
    message: Message, command: CommandObject, bot: Bot
) -> None:
    await send_mailing_command(message, command, bot)


@router.message(Command("delchat"))
async def del_chat_command_root(message: Message) -> None:
    await del_chat_command(message)


@router.message(Command("confirms"))
async def show_confirms_command_root(message: Message) -> None:
    await show_confirms_command(message)


@router.message(Command("confirm"))
async def show_confirm_command_root(message: Message, command: CommandObject) -> None:
    await show_confirm_command(message, command)


@router.message(Command("addconfirm"))
async def add_confirm_command_root(
    message: Message, command: CommandObject, bot: Bot
) -> None:
    await add_confirm_command(message, command, bot)


@router.message(Command("endconfirm"))
async def del_confirm_command_root(message: Message, command: CommandObject) -> None:
    await del_confirm_command(message, command)


@router.message(Command("askchat"))
async def show_chat_command_root(message: Message, bot: Bot) -> None:
    await show_chat_command(message, bot)


@router.message(Command("editaboutquiz"))
async def edit_about_quiz_command_root(
    message: Message, command: CommandObject
) -> None:
    await edit_about_quiz_command(message, command)


@router.message(Command("aboutquiz"))
async def show_about_quiz_command_root(message: Message) -> None:
    await show_about_quiz_command(message)


@router.message(Command("editfaq"))
async def edit_faq_command_root(message: Message, command: CommandObject) -> None:
    await edit_faq_command(message, command)


@router.message(Command("faq"))
async def show_faq_command_root(message: Message) -> None:
    await show_faq_command(message)


@router.message(Command("editrules"))
async def edit_rules_command_root(message: Message, command: CommandObject) -> None:
    await edit_rules_command(message, command)


@router.message(Command("rules"))
async def show_rules_command_root(message: Message) -> None:
    await show_rules_command(message)


@router.message(Command("news"))
async def show_news_command_root(message: Message) -> None:
    await show_news_command(message)


@router.message(Command("addnews"))
async def add_news_command_root(message: Message, command: CommandObject) -> None:
    await add_news_command(message, command)


@router.message(Command("editnews"))
async def edit_news_command_root(message: Message, command: CommandObject) -> None:
    await edit_news_command(message, command)


@router.message(Command("delnews"))
async def delete_news_command_root(message: Message, command: CommandObject) -> None:
    await delete_news_command(message, command)


@router.message(Command("quizzes"))
async def show_quizzes_command_root(message: Message) -> None:
    await show_quizzes_command(message)


@router.message(Command("quiz"))
async def show_quiz_command_root(message: Message, command: CommandObject) -> None:
    await show_quiz_command(message, command)


@router.message(Command("addquiz"))
async def add_quiz_command_root(message: Message, command: CommandObject) -> None:
    await add_quiz_command(message, command)


@router.message(Command("editquiz"))
async def edit_quiz_command_root(message: Message, command: CommandObject) -> None:
    await edit_quiz_command(message, command)


@router.message(Command("delquiz"))
async def delete_quiz_command_root(message: Message, command: CommandObject) -> None:
    await delete_quiz_command(message, command)


@router.message()
async def echo_message_root(message: Message) -> None:
    await echo_message(message)
