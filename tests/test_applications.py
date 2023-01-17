import logging

import pytest

from common import admin_api
from common.allure_labels import allure_labels
from common.application import Application
from common.sessions import BaseSession
from conftest import CONFIG
from model.application_manager import ApplicationManager
from uuid import UUID

LOGGER = logging.getLogger(__name__)


@pytest.fixture(scope='function')
def user_session(driver_cookie: dict) -> BaseSession:
    session = BaseSession(driver_cookie)
    return session


@pytest.fixture(scope='function')
def admin_session(admin_cookie: dict) -> BaseSession:
    session = BaseSession(admin_cookie)
    return session


@pytest.fixture(scope='function')
def app(authorization: ApplicationManager) -> ApplicationManager:
    authorization.profile.open()
    return authorization


@pytest.fixture(scope='function')
def teardown_delete_app(user_session: BaseSession, admin_session: BaseSession) -> Application:
    application = Application(CONFIG)

    yield application

    application.delete(user_session)
    admin_api.get_logs(admin_session, CONFIG)


@pytest.fixture(scope='function')
def create_app(user_session: BaseSession, admin_session: BaseSession) -> Application:
    application = Application(CONFIG)\
        .create(user_session)

    yield application

    admin_api.get_logs(admin_session, CONFIG)


def test_create_application(app, teardown_delete_app):
    allure_labels(feature='Работа с приложениями',
                  story='Создание приложения',
                  title='Успешное создание приложения')
    app.profile.open_create_application()
    (
        app.create_application
        .fill_form()
        .submit()
    )

    teardown_delete_app.app_href = app.create_application.get_created_application_href()
    assert app.create_application.success_create_text(), 'Нет сообщения о успешном создании приложения'
    assert app.create_application.download_cert_btn()
    olol = app.create_application.client_id()
    client_id = app.create_application.client_id()
    client_secret = app.create_application.client_secret()
    assert app.create_application.is_valid_uuid(client_id), 'client_id не соответствует формату uuid'
    assert app.create_application.is_valid_uuid(client_secret), 'client_secret не соответствует формату uuid'
    assert app.create_application.client_secret_input_type() == 'password',\
        'После создания приложения, client_secret не скрыт точками'
    app.create_application.show_client_secret_btn_click()
    assert app.create_application.client_secret_input_type() == 'text',\
        'После нажатия на кнопку "глаз" client_secret скрыт точками '
    LOGGER.info(f'Создано приложение {teardown_delete_app.app_href}')
    pass


def test_delete_application(create_app, app):
    """
    В ToDo В аргументах test_delete_application важна последовательность указания фикстур
    сначала приложение создается, затем открывается профиль
    Если профиль открывается до создания приложения, то в списке приложений его не будет
    По возможности необходимо переработать
    """
    allure_labels(feature='Работа с приложениями',
                  story='Удаление приложения',
                  title='Успешное удаление приложения')
    app_instance = create_app

    app.profile.go_to_application(app_instance)
    app.application_page.go_to_edit_application(app_instance)
    app.edit_application.delete_application(app_instance)

    assert app.profile.current_url() == app.profile._page_url,\
        'После удаления приложения не открылась страница профиля'
    assert app.profile.application_card_not_exist(app_instance),\
        'Приложение присутствует в профиле, приложение не удалено'
    LOGGER.info(f'Приложение удалено {app_instance.app_href}')

    pass
