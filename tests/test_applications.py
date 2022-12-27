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
    return authorization


@pytest.fixture(scope='function')
def delete_app(portal_session: PortalSession) -> Application:
    application = Application()
    # application.create(portal_session)
    # application.delete(portal_session)
    yield application

    application.delete(portal_session)


# @pytest.fixture(scope='function')
# def create_app(app: ApplicationManager, driver_cookie: dict) -> Application:
#     application = Application(driver_cookie)
#     application.create(app)
#
#     yield application
#
#     # application.delete()


def test_create_application(app, delete_app):
    correct_password = CONFIG.defaults.password
    app.profile.open_create_application()
    (
        app.create_application
            .fill_form(correct_password)
            .submit()
    )

    delete_app.app_href = app.create_application.get_created_application_href()
    LOGGER.info(f'Создано приложение {delete_app.app_href}')
    assert app.create_application.success_create_text(), 'Нет сообщения о успешном создании приложения'
    assert app.create_application.download_cert_btn()
    # olol = app.create_application.client_id()
    assert app.create_application.client_id()
    assert app.create_application.client_secret()
    pass


# def test_delete_application(app, create_app: Application):
#     olol = create_app.app_href
