import time

import pytest

from conftest import CONFIG
from model.application_manager import ApplicationManager


@pytest.fixture(scope='function')
def app(authorization: ApplicationManager) -> ApplicationManager:
    authorization.profile.open()
    return authorization


def test_create_application(app):
    correct_password = CONFIG.defaults.password
    app.profile.open_create_application()
    (
        app.application_create
           .fill_form(correct_password)
           .submit()
    )
    assert app.application_create.success_create_text(), 'Нет сообщения о успешном создании приложения'
    # opop = app.__getattribute__('url')
    # assert app.applications.driver.current_url == app.__getattribute__('url'), 'После нажатия кнопки отмены открылась не та страница'
    pass
    # time.sleep(3)