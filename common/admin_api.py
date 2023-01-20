import logging
from typing import List

import requests
from bs4 import BeautifulSoup
from requests import HTTPError, Response

from common.sessions import BaseSession
from model.models import StandConfig

LOGGER = logging.getLogger(__name__)


def admin_login(config: StandConfig) -> Response:
    try:
        response = requests.get(
            url=f'{config.urls.base_url}/user/login',
            verify=False
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        form_build_id = soup.select('input[name=form_build_id]')[1]['value']

        request_body = {
            'name': f'{config.users.admin.login}',
            'pass': f'{config.users.admin.password}',
            'form_build_id': f'{form_build_id}',
            'form_id': 'user_login_form',
            'op': 'Log in'
        }
        response = requests.post(
            url=f'{config.urls.base_url}/user/login',
            data=request_body,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            verify=False
        )
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        assert soup.select('#toolbar-item-user'), 'Не удалось залогиниться администратором'
    except (HTTPError, AssertionError) as e:
        LOGGER.exception(f'Ошибка логина {e}')
        raise
    else:
        return response


def get_admin_cookie(config: StandConfig) -> dict:
    response = admin_login(config)
    admin_cookie = dict(name=f'{response.cookies.keys()[0]}', value=f'{response.cookies.values()[0]}')
    return admin_cookie


def get_logs(session: BaseSession, config: StandConfig) -> List:
    with session as s:
        response = s.get(f'{config.urls.base_url}/admin/sbt/request-log/json')
        log = response.json()
        return log
