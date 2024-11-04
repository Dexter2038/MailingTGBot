from os import environ
from app.database.models import init_db
from app.utils.mailing import init_mailing
from app.utils.ranks import init_rank_files


def initialize_app() -> None:
    """
    Инициализация приложения.

    Эта функция инициализирует базу данных, почтовый сервис и систему рангов.
    """
    try:
        # Инициализация базы данных
        init_db()

        # Инициализация почтового сервиса
        init_mailing()

        # Инициализация системы рангов
        init_rank_files(environ["ADMIN"])

    except Exception as e:
        print(e)
        exit()
