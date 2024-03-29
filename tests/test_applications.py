import logging
import time

import allure
import pytest

from common import admin_api
from common.allure_labels import allure_labels
from common.application import Application
from common.sessions import BaseSession
from conftest import CONFIG
from model.application_manager import ApplicationManager

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
    application = Application(CONFIG) \
        .create(user_session)

    yield application

    admin_api.get_logs(admin_session, CONFIG)


@pytest.fixture(scope='function')
def create_and_delete_app(user_session: BaseSession, admin_session: BaseSession) -> Application:
    application = Application(CONFIG) \
        .create(user_session)

    yield application

    application.delete(user_session)
    admin_api.get_logs(admin_session, CONFIG)


@pytest.fixture(scope='function')
def subscription_and_select_app(app: ApplicationManager) -> str:
    app.main_page.open_catalog()
    app.catalog.select_product()
    app.subscription.select_tariff()
    app.subscription.select_app_from_list()
    app.create_application.fill_form()
    app.subscription.subs_btn_next_click()
    app_name = app.subscription.get_name_app()
    app.subscription.subs_btn_next_click()
    app.profile.open()
    app_href = app.profile.get_app_href_by_name(app_name)
    return app_href


def test_create_application(app: ApplicationManager, teardown_delete_app: Application):
    allure_labels(feature='Работа с приложениями',
                  story='Создание приложения',
                  title='Успешное создание приложения')
    with allure.step('Открыть список всех приложений'):
        app.profile.open_create_application()
    with allure.step('Заполнение формы и создание приложения'):
        (
            app.create_application
                .fill_form()
                .submit()
        )

    teardown_delete_app.app_href = app.create_application.get_created_application_href()

    with allure.step('Проверка созданного приложения'):
        assert app.create_application.success_create_text(), 'Нет сообщения о успешном создании приложения'
        # assert app.create_application.download_cert_btn()
        client_id = app.create_application.client_id()
        client_secret = app.create_application.client_secret()
        assert app.create_application.is_valid_uuid(client_id), 'client_id не соответствует формату uuid'
        assert app.create_application.is_valid_uuid(client_secret), 'client_secret не соответствует формату uuid'
        assert app.create_application.client_secret_input_type() == 'password', \
            'После создания приложения, client_secret не скрыт точками'
        app.create_application.show_client_secret_btn_click()
        assert app.create_application.client_secret_input_type() == 'text', \
            'После нажатия на кнопку "глаз" client_secret скрыт точками '
        app.profile.open()
        app_href = teardown_delete_app.app_href
        assert app.profile.find_create_app(app_href), 'Созданное приложение отсутствует в списке приложений профиля'

    LOGGER.info(f'Создано приложение {teardown_delete_app.app_href}')
    pass


def test_revoke_certificate(app: ApplicationManager, create_and_delete_app: Application):
    allure_labels(feature='Работа с приложениями',
                  story='Работа с сертификатом',
                  title='Успешный отзыв сертификата')
    app_instance = create_and_delete_app
    with allure.step('Открыть список всех приложений'):
        app.profile.open()
    with allure.step('Открыть созданное приложение'):
        app.profile.go_to_application(app_instance)
    with allure.step('Переход на страницу сертификаты'):
        app.application_page.go_to_certificates()
        cert_id = app.app_certificate.get_cert_id()
    with allure.step('Отозвать сертификат'):
        app.app_certificate.revoke_certificate_click()
        app.app_certificate.select_another_reason_revoke_sert()
        app.app_certificate.submit_revoke()

    with allure.step('Проверка отозванного сертификата'):
        assert app.app_certificate.success_text_panel(), 'Нет сообщения "Сертификат успешно отозван"'
        assert app.app_certificate.is_status_cert_revoked(cert_id), \
            f'У сертификата "{cert_id}" не отображен статус "отозван"'

    LOGGER.info(f'Сертификат {cert_id} успешно отозван')
    pass


def test_issue_new_certificate(app: ApplicationManager, create_and_delete_app: Application):
    allure_labels(feature='Работа с приложениями',
                  story='Работа с сертификатом',
                  title='Успешный перевыпуск сертификата')
    """
    Todo вынести отзыв сертификата в работу через АПИ
    """
    app_instance = create_and_delete_app
    with allure.step('Открыть список всех приложений'):
        app.profile.open()
    with allure.step('Открыть созданное приложение'):
        app.profile.go_to_application(app_instance)
    with allure.step('Переход на страницу "сертификаты"'):
        app.application_page.go_to_certificates()
    with allure.step('Отозвать сертификат'):
        app.app_certificate.revoke_certificate_click()
        app.app_certificate.select_another_reason_revoke_sert()
        app.app_certificate.submit_revoke()
    with allure.step('Выпуск нового сертификата'):
        app.app_certificate.issue_new_certificate_click()
        app.app_certificate.type_defaults_password()
        app.app_certificate.submit()

    with allure.step('Проверка заголовка о готовности сертификата'):
    # assert app.app_certificate_page.download_cert_btn()
        assert app.app_certificate.success_text_panel(), 'Нет сообщения "Сертификат готов"'

    LOGGER.info('Сертификат успешно выпущен')
    pass


def test_get_new_client_secret(app: ApplicationManager, create_and_delete_app: Application):
    allure_labels(feature='Работа с приложениями',
                  story='Работа с ключами',
                  title='Успешный сброс client_secret')
    app_instance = create_and_delete_app
    with allure.step('Открыть список всех приложений'):
        app.profile.open()
    with allure.step('Открыть созданное приложение'):
        app.profile.go_to_application(app_instance)
    with allure.step('Переход на страницу "ключи"'):
        app.application_page.go_to_keys()
    with allure.step('Выпуск нового ClientSecret'):
        app.app_keys.get_new_client_secret_link_click()
        app.app_keys.get_new_client_secret_btn_click()

        client_secret = app.app_keys.client_secret()
    with allure.step('Проверка нового ClientSecret'):
        assert app.app_keys.allert_info(), 'Нет сообщения "Обратите внимание ..."'
        assert app.app_keys.notice(), 'Нет предупреждения "Обязательно сохраните куда-нибудь clientSecret ..."'
        assert app.app_keys.is_valid_uuid(client_secret), 'client_secret не соответствует формату uuid'
        assert app.app_keys.client_secret_input_type() == 'password', \
            'После перевыпуска client_secret, он не скрыт точками'
        app.app_keys.show_client_secret_btn_click()
        assert app.app_keys.client_secret_input_type() == 'text', \
            'После нажатия на кнопку "глаз" client_secret скрыт точками '

    LOGGER.info(f'Client_secret успешно получен {client_secret}')
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
    with allure.step('Открыть созданное приложение'):
        app.profile.go_to_application(app_instance)
    with allure.step('Переход в настройки приложения'):
        app.application_page.go_to_edit_application(app_instance)
    with allure.step('Удаление приложения'):
        app.edit_application.delete_application(app_instance)

    with allure.step('Проверка что приложение удалено'):
        assert app.profile.current_url() == app.profile._page_url, \
            'После удаления приложения не открылась страница профиля'
        assert app.profile.application_card_not_exist(app_instance), \
            'Приложение присутствует в профиле, приложение не удалено'
    LOGGER.info(f'Приложение удалено {app_instance.app_href}')

    pass


def test_subscription(app: ApplicationManager, create_and_delete_app: Application):
    allure_labels(feature='Работа с приложениями',
                  story='Оформление подписки для существующего приложения',
                  title='Успешное оформление подписки для существующего приложения')
    app_instance = create_and_delete_app
    with allure.step('Открыть список всех приложений'):
        app.profile.open()
    with allure.step('Открыть созданное приложение'):
        app.profile.go_to_application(app_instance)
        app_name = app.application_page.get_name_app()
    with allure.step('Переход в каталог продуктов'):
        app.application_page.go_to_catalog()
    with allure.step('Переход в продукт'):
        app.catalog.select_product()
    with allure.step('Выбор тарифа'):
        app.subscription.select_tariff()
    with allure.step('Выбор приложения и оформление подписки'):
        app.subscription.select_app_from_list(app_name)

    with allure.step('Проверка оформленной подписки'):
        assert app.subscription.title_alert(), 'Нет сообщения "Подписка готова"'


def test_subscribing_and_creating_an_app(app: ApplicationManager, teardown_delete_app: Application):
    allure_labels(feature='Работа с приложениями',
                  story='Оформление подписки и создание приложения во время оформления подписки',
                  title='Успешное оформление подписки и создание приложения')

    with allure.step('Переход в каталог продуктов'):
        app.main_page.open_catalog()
    with allure.step('Переход в продукт'):
        app.catalog.select_product()
    with allure.step('Выбор тарифа'):
        app.subscription.select_tariff()
    with allure.step('Создание нового прижения'):
        app.subscription.select_app_from_list()
        app.create_application.fill_form()
        app.subscription.subs_btn_next_click()
        app_name = app.subscription.get_name_app()

    with allure.step('Проверка созданного приложения'):
        assert app.subscription.title_alert(), 'Нет сообщений "Приложение создано" "Сертификат выпущен"'

    with allure.step('Оформление подписки'):
        app.subscription.subs_btn_next_click()

    with allure.step('Проверки созданного приложения и оформленной подписки'):
        assert app.subscription.title_alert(), 'Нет сообщения "Подписка готова"'
        client_id = app.create_application.client_id()
        client_secret = app.create_application.client_secret()
        assert app.create_application.is_valid_uuid(client_id), 'client_id не соответствует формату uuid'
        assert app.create_application.is_valid_uuid(client_secret), 'client_secret не соответствует формату uuid'
        assert app.create_application.client_secret_input_type() == 'password', \
            'После создания приложения, client_secret не скрыт точками'
        app.create_application.show_client_secret_btn_click()
        assert app.create_application.client_secret_input_type() == 'text', \
            'После нажатия на кнопку "глаз" client_secret скрыт точками '

    app.profile.open()
    teardown_delete_app.app_href = app.profile.get_app_href_by_name(app_name)


def test_unsubscribe(app: ApplicationManager, subscription_and_select_app, teardown_delete_app: Application):
    allure_labels(feature='Работа с приложениями',
                  story='Остановить подписку у созданного приложения во время оформления подписки',
                  title='Успешная отписка от продукта')
    app_href = subscription_and_select_app
    with allure.step('Открыть созданное приложение'):
        app.profile.open_created_app_during_subscription(app_href)
    with allure.step('Переход в карточку продукта'):
        app.create_application.product_card_click()
    with allure.step('Отписка от продукта'):
        app.product.stop_subs_click()
        app.subscription.submit_click()

    assert app.subscription.title_alert(), 'Нет сообщения "Подписка удалена успешно"'

    teardown_delete_app.app_href = app_href
