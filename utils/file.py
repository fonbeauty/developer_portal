import json

from datetime import datetime
from pathlib import Path

from model.data_model.config import User


def path_for_resources(file_name='') -> str:
    path = str(Path(__file__).parent.parent.joinpath('resources').joinpath(file_name))
    return path


def path_for_cookies(file_name='') -> str:
    path = str(Path(path_for_resources('cookies')).joinpath(file_name))
    return path


def cookie_write(stand: str, user: str, cookie: dict):
    cookie['creation_time'] = str(datetime.now())
    with open(path_for_cookies(f'{stand}_{user}.txt'), 'w') as file:
        json.dump(cookie, file)


def cookie_read(stand: str, user: str) -> dict:
    try:
        with open(path_for_cookies(f'{stand}_{user}.txt'), 'r') as json_file:
            data = json.load(json_file)
        return data
    except FileNotFoundError:
        return None


def cookie_expired_from_file(stand: str, user: str, expire_time: int) -> bool:
    creation_time_string = (cookie_read(stand, user).get('creation_time'))
    format_datetime = "%Y-%m-%d %H:%M:%S.%f"
    creation_time = datetime.strptime(creation_time_string, format_datetime)
    current_time = datetime.now()
    if (current_time - creation_time).total_seconds() <= expire_time:
        return False
    else:
        return True


def is_cookie_expired(stand: str, user: User, expire_time: int) -> bool:
    creation_time_string = user.cookie.get('creation_time')
    format_datetime = "%Y-%m-%d %H:%M:%S.%f"
    creation_time = datetime.strptime(creation_time_string, format_datetime)
    current_time = datetime.now()
    if (current_time - creation_time).total_seconds() <= expire_time:
        return False
    else:
        return True


def get_cookie() -> dict:
    pass
