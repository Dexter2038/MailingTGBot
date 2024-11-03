from asynctinydb import TinyDB


DB_PATH = "database.json"  # Путь к базе данных


def get_db() -> TinyDB:
    """Создает и возвращает объект базы данных TinyDB.

    Returns:
        TinyDB: Объект базы данных.
    """
    return TinyDB(DB_PATH)


async def edit_about_quiz(text: str) -> bool:
    """Редактирует единственную запись about_quiz.

    Args:
        text (str): Новый текст для about_quiz.

    Returns:
        bool: True, если запись была успешно добавлена, иначе False.
    """
    async with get_db() as db:
        quiz_info = db.table("quiz_info")
        await quiz_info.truncate()
        return bool(await quiz_info.insert({"text": text}))


async def get_about_quiz() -> str | None:
    """Получает единственную запись about_quiz.

    Returns:
        str|None: Текст about_quiz, если запись существует, иначе None.
    """
    async with get_db() as db:
        quiz_info = db.table("quiz_info")
        records = await quiz_info.all()
        return records[0].get("text") if records else None


async def edit_faq(text: str) -> bool:
    """Редактирует единственную запись FAQ.

    Args:
        text (str): Новый текст для FAQ.

    Returns:
        bool: True, если запись была успешно добавлена, иначе False.
    """
    async with get_db() as db:
        faq = db.table("faq")
        await faq.truncate()
        return bool(await faq.insert({"text": text}))


async def get_faq() -> str | None:
    """Получает единственную запись FAQ.

    Returns:
        str|None: Текст FAQ, если запись существует, иначе None.
    """
    async with get_db() as db:
        faq = db.table("faq")
        records = await faq.all()
        return records[0].get("text") if records else None


async def add_news(text: str) -> int:
    """Добавляет новость в базу данных и удаляет самую старую, если их больше 5.

    Args:
        text (str): Текст новости.

    Returns:
        int: ID добавленной новости.
    """
    async with get_db() as db:
        news_table = db.table("news")

        # Проверяем количество новостей
        if len(await news_table.all()) >= 5:
            # Удаляем самую старую новость
            oldest_news = await news_table.all()
            await news_table.remove(doc_ids=[oldest_news[0].doc_id])

        # Добавляем новую новость
        news_id = await news_table.insert({"text": text})
        return news_id


async def edit_news(id: int, text: str) -> bool:
    """Редактирует новость по ID.

    Args:
        id (int): ID записи.
        text (str): Новый текст для новости.

    Returns:
        bool: True, если новость была успешно обновлена, иначе False.
    """
    async with get_db() as db:
        news = db.table("news")
        updated_ids = await news.update({"text": text}, doc_ids=[int(id)])
        return bool(updated_ids)  # Проверка на наличие обновленных записей


async def get_news_admin() -> list:
    """Получает все новости для админа.

    Returns:
        list: Список всех записей новостей. Элемент списка - кортеж (ID, текст новости).
    """
    async with get_db() as db:
        news = db.table("news")
        return [(item.doc_id, item["text"]) for item in await news.all()]


async def get_news_user() -> list:
    """Получает все новости для пользователя.

    Returns:
        list: Список всех записей новостей. Элемент списка - текст новости.
    """
    async with get_db() as db:
        news = db.table("news")
        return [item["text"] for item in await news.all()]


async def get_news_one(id: int | str) -> str | None:
    """Получает единственную запись новости по ID.

    Args:
        id (int): ID новости.

    Returns:
        str|None: Текст новости, если запись существует, иначе None.
    """
    async with get_db() as db:
        news = db.table("news")
        records = await news.get(doc_id=id)
        return (records.doc_id, records.get("text")) if records else None


async def del_news(id: int) -> bool:
    """Удаляет новость по ID.

    Args:
        id (int): ID новости для удаления.

    Returns:
        bool: True, если новость была успешно удалена, иначе False.
    """
    async with get_db() as db:
        news = db.table("news")
        removed_ids = await news.remove(doc_ids=[int(id)])
        return bool(removed_ids)  # Проверка на наличие удаленных записей


async def get_quizzes_admin() -> list:
    """Получает все викторины для админа.

    Returns:
        list: Список всех записей викторин. Элемент списка - кортеж (ID, текст викторины).
    """
    async with get_db() as db:
        quizzes = db.table("quizzes")
        return [(item.doc_id, item["text"]) for item in await quizzes.all()]


async def get_quizzes_user() -> list:
    """Получает все викторины для пользователя.

    Returns:
        list: Список всех записей викторин. Элемент списка - текст викторины.
    """
    async with get_db() as db:
        quizzes = db.table("quizzes")
        return [item["text"] for item in await quizzes.all()]


async def get_quiz(id: int) -> str | None:
    """Получает единственную запись викторины по ID.

    Args:
        id (int): ID викторины для получения.

    Returns:
        str|None: Текст викторины, если запись существует, иначе None.
    """
    async with get_db() as db:
        quizzes = db.table("quizzes")
        records = await quizzes.get(doc_id=int(id))
        return records.get("text") if records else None


async def add_quiz(text: str) -> int:
    """Добавляет викторину в базу данных и удаляет самую старую, если их больше 5.

    Args:
        text (str): Текст викторины.

    Returns:
        int: ID добавленной викторины.
    """
    async with get_db() as db:
        quizzes_table = db.table("quizzes")

        # Проверяем количество викторин
        if len(await quizzes_table.all()) >= 5:
            # Удаляем самую старую викторину
            oldest_quiz = await quizzes_table.all()
            await quizzes_table.remove(doc_ids=[oldest_quiz[0].doc_id])

        # Добавляем новую викторину
        quiz_id = await quizzes_table.insert({"text": text})
        return quiz_id


async def edit_quiz(id: int, text: str) -> bool:
    """Редактирует викторину по ID.

    Args:
        id (int): ID записи.
        text (str): Новый текст для викторины.

    Returns:
        bool: True, если викторина была успешно обновлена, иначе False.
    """
    async with get_db() as db:
        quizzes = db.table("quizzes")
        updated_ids = await quizzes.update({"text": text}, doc_ids=[int(id)])
        return bool(updated_ids)  # Проверка на наличие обновленных записей


async def del_quiz(id: int) -> bool:
    """Удаляет викторину по ID.

    Args:
        id (int): ID викторины для удаления.

    Returns:
        bool: True, если викторина была успешно удалена, иначе False.
    """
    async with get_db() as db:
        quizzes = db.table("quizzes")
        removed_ids = await quizzes.remove(doc_ids=[int(id)])
        return bool(removed_ids)  # Проверка на наличие удаленных записей
