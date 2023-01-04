import json

from datetime import datetime
from pathlib import Path


def path_for_resources(file_name='') -> str:
    path = str(Path(__file__).parent.parent.joinpath('resources').joinpath(file_name))
    return path


def path_for_cookies(file_name='') -> str:
    path = str(Path(path_for_resources('cookies')).joinpath(file_name))
    return path


def cookie_write(stand: str, user_session_id: str, cookie: dict):
    cookie['creation_time'] = str(datetime.now())
    with open(path_for_cookies(f'{stand}_{user_session_id}.txt'), 'w') as file:
        json.dump(cookie, file)


def cookie_read(stand: str, user_session_id: str) -> dict:
    try:
        with open(path_for_cookies(f'{stand}_{user_session_id}.txt'), 'r') as json_file:
            data = json.load(json_file)
        return data
    except FileNotFoundError:
        return None


def cookie_expired(stand: str, user_session_id: str, expire_time: int) -> bool:
    creation_time_string = (cookie_read(stand, user_session_id).get('creation_time'))
    format_datetime = "%Y-%m-%d %H:%M:%S.%f"
    creation_time = datetime.strptime(creation_time_string, format_datetime)
    current_time = datetime.now()

    if (current_time - creation_time).total_seconds() <= expire_time:
        return False
    else:
        return True


