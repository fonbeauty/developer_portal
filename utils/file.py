import json

from datetime import datetime
from pathlib import Path


def path_forresources(file_name='') -> str:
    path = str(Path(__file__).parent.parent.joinpath('resources').joinpath(file_name))
    return path


def cookie_write(cookie: dict):
    cookie['creation_time'] = str(datetime.now())
    with open('cookie.txt', 'w') as file:
        json.dump(cookie, file)


def cookie_read() -> dict:
    try:
        with open('cookie.txt', 'r') as json_file:
            data = json.load(json_file)
        return data
    except FileNotFoundError:
        return None


def cookie_expired(expire_time: int) -> bool:
    creation_time_string = (cookie_read().get('creation_time'))
    format_datetime = "%Y-%m-%d %H:%M:%S.%f"
    creation_time = datetime.strptime(creation_time_string, format_datetime)
    current_time = datetime.now()

    if (current_time - creation_time).seconds <= expire_time:
        return False
    else:
        return True


