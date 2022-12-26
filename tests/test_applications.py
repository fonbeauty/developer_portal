import logging
import time
import uuid

import pytest
import requests

from bs4 import BeautifulSoup

from conftest import CONFIG
from model.application_manager import ApplicationManager

LOGGER = logging.getLogger(__name__)


class Application:

    def __init__(self, driver_cookie: dict):
        self.password = CONFIG.defaults.password
        self.app_description = 'Приложение создано автотестами, можно удалить' \
                               'Application was created by autotests, it may be deleted'
        self.app_name = f'autotest_{uuid.uuid4()}'
        self.driver_cookie = driver_cookie
        self.app_id = ''

    def create(self):
        with requests.Session() as s:
            headers = {'Content-Type': 'application/x-www-form-urlencoded',
                       'cookie': f'{self.driver_cookie["name"]}={self.driver_cookie["value"]}'}

            response = s.get(
                url=f'{CONFIG.urls.base_url}/profile/{CONFIG.users.developer.space}/app/create',
                headers=headers,
                verify=False
            )
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            form_build_id = soup.select('input[name=form_build_id]')[0]['value']
            form_token = soup.select('input[name=form_token]')[0]['value']

            request_body = {
                'app_name': f'autotest_{uuid.uuid4()}',
                'app_description': 'Приложение создано автотестами, можно удалить'
                                   'Application was created by autotests, it may be deleted',
                'oauth[]': '',
                'password': CONFIG.defaults.password,
                'password_confirm': CONFIG.defaults.password,
                'form_build_id': f'{form_build_id}',
                'form_token': f'{form_token}',
                'form_id': 'application_create_download_cert_form',
                'save': 'создать'
            }

            response = s.post(
                url=f'{CONFIG.urls.base_url}/profile/{CONFIG.users.developer.space}/app/create',
                data=request_body
            )
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            self.app_id = f'{CONFIG.urls.base_url}{soup.select("#edit-to-app")[0]["href"]}'
            LOGGER.info(f'Создано приложение {self.app_id}')
        pass

    def delete(self):
        with requests.Session() as s:
            headers = {'Content-Type': 'application/x-www-form-urlencoded',
                       'cookie': f'{self.driver_cookie["name"]}={self.driver_cookie["value"]}'}

            response = s.get(
                url=f'{self.app_id}/delete',
                headers=headers,
                verify=False
            )
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            form_build_id = soup.select('input[name=form_build_id]')[0]['value']
            form_token = soup.select('input[name=form_token]')[0]['value']

            request_body = {
                # 'op': 'да, хочу',
                # 'confirm': 1,
                'form_build_id': f'{form_build_id}',
                'form_token': f'{form_token}',
                'form_id': 'application_delete'
            }

            delete_response = s.post(
                url=f'{self.app_id}/delete',
                data=request_body
            )
            delete_response.raise_for_status()
            LOGGER.info(f'Приложение удалено {self.app_id}')
        pass


@pytest.fixture(scope='function')
def app(authorization: ApplicationManager) -> ApplicationManager:
    authorization.profile.open()
    return authorization


@pytest.fixture(scope='function')
def delete_app(driver_cookie: dict) -> Application:
    application = Application(driver_cookie)

    yield application

    application.delete()


@pytest.fixture(scope='function')
def create_app(app: ApplicationManager, driver_cookie: dict) -> Application:
    application = Application(driver_cookie)
    application.create(app)

    yield application

    # application.delete()


def test_create_application(app, delete_app):
    correct_password = CONFIG.defaults.password
    app.profile.open_create_application()
    (
        app.create_application
            .fill_form(correct_password)
            .submit()
    )

    delete_app.app_id = app.create_application.get_created_application_href()
    LOGGER.info(f'Создано приложение {delete_app.app_id}')
    assert app.create_application.success_create_text(), 'Нет сообщения о успешном создании приложения'
    assert app.create_application.download_cert_btn()
    # olol = app.create_application.client_id()
    assert app.create_application.client_id()
    assert app.create_application.client_secret()
    pass
#     # time.sleep(3)


# def test_delete_application(app, create_app: Application):
#     create_app.delete()
