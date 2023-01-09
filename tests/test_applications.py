import logging

import pytest

from common.application import Application
from common.sessions import PortalSession
from conftest import CONFIG
from model.application_manager import ApplicationManager

LOGGER = logging.getLogger(__name__)


@pytest.fixture(scope='function')
def portal_session(driver_cookie: dict) -> PortalSession:
    session = PortalSession(driver_cookie)
    return session


@pytest.fixture(scope='function')
def app(authorization: ApplicationManager) -> ApplicationManager:
    authorization.profile.open()
    authorization.profile.cookie_panel_close()
    return authorization


@pytest.fixture(scope='function')
def teardown_delete_app(portal_session: PortalSession) -> Application:
    application = Application(CONFIG)

    yield application

    application.delete(portal_session)


@pytest.fixture(scope='function')
def create_app(portal_session: PortalSession) -> Application:
    application = Application(CONFIG)\
        .create(portal_session)

    yield application


def test_create_application(app, teardown_delete_app):
    app.profile.open_create_application()
    (
        app.create_application
            .fill_form()
            .submit()
    )

    teardown_delete_app.app_href = app.create_application.get_created_application_href()
    assert app.create_application.success_create_text(), 'Нет сообщения о успешном создании приложения'
    assert app.create_application.download_cert_btn()
    # olol = app.create_application.client_id()
    assert app.create_application.client_id()
    assert app.create_application.client_secret()
    LOGGER.info(f'Создано приложение {teardown_delete_app.app_href}')
    pass


def test_delete_application(create_app, app):
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
