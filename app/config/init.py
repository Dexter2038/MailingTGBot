from os import environ
from app.database.models import init_db
from app.utils.ranks import init_rank_files
from app.utils.client import init_client


def initialize_app() -> None:
    """
    Инициализация приложения.

    Эта функция инициализирует базу данных, почтовый сервис и систему рангов.
    """
    try:
        # Инициализация базы данных
        init_db()

        # Инициализация системы рангов
        init_rank_files(environ["ADMIN"])

        # Инициализация MTProto API
        init_client()

    except Exception as e:
        print(e)
        print("Не удалось инициализировать приложение")
        exit()
