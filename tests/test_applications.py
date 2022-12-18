import time

import pytest
import requests

from bs4 import BeautifulSoup

from conftest import CONFIG
from model.application_manager import ApplicationManager


class App:

    app_id: str

    # def create(self, id: str ):
    #     self.app_id = id
    #     pass
    #
    # def cleanup(self):
    #     olol = self.app_id
    #     print(olol)
    #     pass


@pytest.fixture(scope='function')
def app(authorization: ApplicationManager) -> ApplicationManager:
    authorization.profile.open()
    return authorization


@pytest.fixture(scope='function')
def create_app(driver_cookie: dict) -> App:
    app_instance = App()

    yield app_instance

    delete_url = f'{app_instance.app_id}/delete'

    with requests.Session() as s:
        cookie_header = {'cookie': f'{driver_cookie["name"]}={driver_cookie["value"]}'}
        content_type_header = {'Content-Type': 'application/x-www-form-urlencoded'}
        result_headers = {**content_type_header, **cookie_header}

        response = s.get(
            url=delete_url,
            headers=result_headers,
            verify=False)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        form_build_id = soup.select('input[name=form_build_id]')[0]['value']
        form_token = soup.select('input[name=form_token]')[0]['value']

        request_body = {
            'op': 'да, хочу',
            'confirm': 1,
            'form_build_id': f'{form_build_id}',
            'form_token': f'{form_token}',
            'form_id': 'application_delete'
        }

        delete_response = s.post(
            url=delete_url,
            headers=result_headers,
            verify=False,
            data=request_body
        )


def has_class_but_no_id(tag):
    return tag.input and tag.has_attr('data-drupal-selector')


def test_create_application(app, create_app: App):

    correct_password = CONFIG.defaults.password
    app.profile.open_create_application()
    (
        app.create_application
           .fill_form(correct_password)
           .submit()
    )

    create_app.app_id = app.create_application.get_created_application_href()
    assert app.create_application.success_create_text(), 'Нет сообщения о успешном создании приложения'
    # opop = app.__getattribute__('url')
    # assert app.applications.driver.current_url == app.__getattribute__('url'), 'После нажатия кнопки отмены открылась не та страница'
    pass
    # time.sleep(3)