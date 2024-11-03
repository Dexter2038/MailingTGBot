from aiogram import Bot, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.database.actions import add_confirm, end_confirm

from app.states.admin import Admin
from app.utils.info import add_quiz, edit_about_quiz, edit_faq, edit_news, edit_quiz
from app.utils.mailing import make_mailing
from app.utils.ranks import add_moder, del_moder
from app.keyboards.admin import get_back_kb


router = Router(name="admin_states")


@router.message(Admin.add_moderator)
async def add_moder_state(message: Message, state: FSMContext) -> None:
    args = message.text.split(" ")

    if len(args) != 2 or not args[0].isdigit():
        await message.answer(
            "Неверный формат. Введите <id> <username> с пробелом между ними. Пример: 123 @username или 123 username",
            reply_markup=get_back_kb(),
        )
        return

    id, username = args

    username = username.replace("@", "")

    try:
        result = await add_moder(id, username)

        if result:
            await message.answer(
                "Пользователь назначен модератором", reply_markup=get_back_kb()
            )
        else:
            await message.answer(
                "Пользователь уже модератор", reply_markup=get_back_kb()
            )

    except Exception:
        await message.answer(
            "Пользователь не назначен модератором. Произошла ошибка",
            reply_markup=get_back_kb(),
        )

    await state.clear()


@router.message(Admin.del_moderator)
async def del_moder_state(message: Message, state: FSMContext) -> None:
    args = message.text.split(" ")

    if len(args) != 1:
        await message.answer(
            "Неверный формат. Введите <id/username> с пробелом между ними. Пример: 123 @username или 123 username",
            reply_markup=get_back_kb(),
        )
        return

    id = args[0]

    try:
        result = await del_moder(id)

        if result:
            await message.answer(
                "Пользователь удален из списка модераторов", reply_markup=get_back_kb()
            )
        else:
            await message.answer(
                "Пользователь не модератор", reply_markup=get_back_kb()
            )

    except Exception:
        await message.answer(
            "Пользователь не удален из списка модераторов. Произошла ошибка",
            reply_markup=get_back_kb(),
        )

    await state.clear()


@router.message(Admin.make_mailing)
async def make_mailing_state(message: Message, state: FSMContext, bot: Bot) -> None:
    text = message.text

    try:
        result = await make_mailing(text, bot)

        if result:
            await message.answer("Рассылка запущена", reply_markup=get_back_kb())
        else:
            await message.answer("Рассылка не запущена", reply_markup=get_back_kb())

    except Exception:
        await message.answer(
            "Рассылка не запущена. Произошла ошибка", reply_markup=get_back_kb()
        )

    await state.clear()


@router.message(Admin.add_news)
async def add_news_state(message: Message, state: FSMContext) -> None:
    text = message.text

    try:
        result = await edit_news(text)

        if result:
            await message.answer("Новости добавлены", reply_markup=get_back_kb())
        else:
            await message.answer("Новости не добавлены", reply_markup=get_back_kb())

    except Exception:
        await message.answer(
            "Новости не добавлены. Произошла ошибка", reply_markup=get_back_kb()
        )

    await state.clear()


@router.message(Admin.add_quiz)
async def add_quiz_state(message: Message, state: FSMContext) -> None:
    text = message.text

    try:
        result = await add_quiz(text)

        if result:
            await message.answer("Викторина добавлена", reply_markup=get_back_kb())
        else:
            await message.answer("Викторина не добавлена", reply_markup=get_back_kb())

    except Exception:
        await message.answer(
            "Викторина не добавлена. Произошла ошибка", reply_markup=get_back_kb()
        )

    await state.clear()


@router.message(Admin.add_confirm)
async def add_confirm_state(message: Message, state: FSMContext) -> None:
    text = message.text

    try:
        result = add_confirm(text)

        if result:
            await message.answer(
                "Рассылка с подтверждением выполнена", reply_markup=get_back_kb()
            )
        else:
            await message.answer(
                "Рассылка с подтверждением не выполнена", reply_markup=get_back_kb()
            )

    except Exception:
        await message.answer(
            "Рассылка с подтверждением не выполнена. Произошла ошибка",
            reply_markup=get_back_kb(),
        )

    await state.clear()


@router.message(Admin.del_confirm)
async def del_confirm_state(message: Message, state: FSMContext) -> None:
    text = message.text

    if not text.isdigit():
        await message.answer(
            "Неверный формат. Введите ID рассылки", reply_markup=get_back_kb()
        )
        return

    try:
        result = await end_confirm(int(text))

        if result:
            await message.answer("Рассылка закончена", reply_markup=get_back_kb())
        else:
            await message.answer("Рассылка не закончена", reply_markup=get_back_kb())

    except Exception:
        await message.answer(
            "Рассылка не закончена. Произошла ошибка", reply_markup=get_back_kb()
        )

    await state.clear()


@router.message(Admin.edit_about_quiz)
async def edit_about_quiz_state(message: Message, state: FSMContext) -> None:
    text = message.text

    try:
        result = await edit_about_quiz(text)

        if result:
            await message.answer("О викторине изменено", reply_markup=get_back_kb())
        else:
            await message.answer("О викторине не изменено", reply_markup=get_back_kb())

    except Exception:
        await message.answer(
            "О викторине не изменено. Произошла ошибка", reply_markup=get_back_kb()
        )

    await state.clear()


@router.message(Admin.edit_faq)
async def edit_faq_state(message: Message, state: FSMContext) -> None:
    text = message.text

    try:
        result = await edit_faq(text)

        if result:
            await message.answer("Частые вопросы изменены", reply_markup=get_back_kb())
        else:
            await message.answer(
                "Частые вопросы не изменены", reply_markup=get_back_kb()
            )

    except Exception:
        await message.answer(
            "Частые вопросы не изменены. Произошла ошибка", reply_markup=get_back_kb()
        )

    await state.clear()


@router.message(Admin.edit_news)
async def edit_news_state(message: Message, state: FSMContext) -> None:
    text = message.text

    data = await state.get_data()

    id = data.get("id", None)

    try:
        result = await edit_news(id, text)

        if result:
            await message.answer("Новости изменены", reply_markup=get_back_kb())
        else:
            await message.answer("Новости не изменены", reply_markup=get_back_kb())

    except Exception:
        await message.answer(
            "Новости не изменены. Произошла ошибка", reply_markup=get_back_kb()
        )

    await state.clear()


@router.message(Admin.edit_quiz)
async def edit_quiz_state(message: Message, state: FSMContext) -> None:
    text = message.text

    data = await state.get_data()

    id = data.get("id", None)

    try:
        result = await edit_quiz(id, text)

        if result:
            await message.answer("Викторина изменена", reply_markup=get_back_kb())
        else:
            await message.answer("Викторина не изменена", reply_markup=get_back_kb())

    except Exception:
        await message.answer(
            "Викторина не изменена. Произошла ошибка", reply_markup=get_back_kb()
        )

    await state.clear()
