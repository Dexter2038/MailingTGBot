import re


def validate_email(email: str) -> bool:
    email_regex = re.compile(
        pattern=r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$"
    )

    return email_regex.match(string=email)
