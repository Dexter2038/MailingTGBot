from mysql.connector import connect, Error
from os import environ


def init_db() -> None:
    try_db_connection()
    setup_models()


def try_db_connection() -> None:
    try:
        with connect(
            host=environ["DB_HOST"],
            user=environ["DB_USER"],
            password=environ["DB_PASSWORD"],
        ) as connection:
            query: str = (
                """
                CREATE DATABASE IF NOT EXISTS %s;
                """
                % (environ["DB_NAME"],)
            )
            with connection.cursor() as cursor:
                cursor.execute(query)
            print("БД успешно инициализирована")
    except KeyError as e:
        print(e)
        print("Невозможно инициализировать БД, не нашли переменную окружения")
        exit(code=403)
    except Error as e:
        print(e)
        print("БД не получилось инициализировать")
        exit(code=403)


def setup_models() -> None:
    try:
        with connect(
            host=environ["DB_HOST"],
            user=environ["DB_USER"],
            password=environ["DB_PASSWORD"],
            database=environ["DB_NAME"],
        ) as connection:
            users_query: str = (
                """
                CREATE TABLE IF NOT EXISTS users (
                    id BIGINT PRIMARY KEY,
                    email VARCHAR(255),
                    username VARCHAR(255)
                );
                """
            )
            confirms_query: str = (
                """
                CREATE TABLE IF NOT EXISTS confirms (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    text VARCHAR(255)
                );
                """
            )
            users_confirms_query: str = (
                """
                CREATE TABLE IF NOT EXISTS users_confirms (
                    user_id BIGINT UNIQUE,
                    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
                    confirm_id INT,
                    FOREIGN KEY (confirm_id) REFERENCES confirms (id) ON DELETE CASCADE
                );
                """
            )
            with connection.cursor() as cursor:
                cursor.execute(users_query)
                cursor.execute(confirms_query)
                cursor.execute(users_confirms_query)
            print("Модели успешно инициализированы")
    except Error as e:
        print(e)
        print("Модели не получилось инициализировать")
        exit(code=403)
