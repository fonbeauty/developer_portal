import time

import pytest

from conftest import CONFIG
from model.application_manager import ApplicationManager


@pytest.fixture(scope='function')
def applications_page(authorization: ApplicationManager) -> ApplicationManager:
    url = f'{CONFIG.base_url}/profile/{CONFIG.developer.space}'
    authorization.main_page.driver.get(url=url)
    authorization.__setattr__('url', url)
    return authorization


def test_create_application(applications_page: ApplicationManager):
    correct_password = CONFIG.default_password
    app = applications_page
    app.applications.go_to_create_application()
    (
        app.application
           .fill_form(correct_password)
           .submit()
    )
    assert app.application.success_create_text(), 'Нет сообщения о успешном создании приложения'
    # opop = app.__getattribute__('url')
    # assert app.applications.driver.current_url == app.__getattribute__('url'), 'После нажатия кнопки отмены открылась не та страница'
    pass
    # time.sleep(3)