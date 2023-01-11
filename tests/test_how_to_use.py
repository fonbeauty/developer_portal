import time

import pytest

from model.application_manager import ApplicationManager

_TEXT = 'token'


@pytest.fixture(scope='function')
def app_main(authorization: ApplicationManager) -> ApplicationManager:
    authorization.main_page.open()
    return authorization


@pytest.fixture(scope='function')
def app(authorization: ApplicationManager) -> ApplicationManager:
    authorization.help_page.open()
    return authorization


def test_open_help_from_header(app_main: ApplicationManager):
    title_name = "О системе"
    app_main.main_page.help_header_link_click()

    assert app_main.help_page.help_title(), 'Заголовок ПОМОЩЬ не найден'
    assert app_main.help_page.doc_title(title_name), 'Требуемый заголовок страницы не найден'


def test_open_help_from_footer(app_main: ApplicationManager):
    app_main.main_page.help_footer_link_click()

    assert app_main.help_page.help_title(), 'Заголовок ПОМОЩЬ не найден'


def test_open_help_contacts(app: ApplicationManager):
    title_name = "Контакты"
    app.help_page.contacts_link_click()

    assert app.help_page.doc_title(title_name), 'Требуемый заголовок страницы не найден'


def test_input_text_search_bar(app: ApplicationManager):
    title_name = "Результаты поиска"
    app.help_page.input_text_search_bar(_TEXT)

    assert app.help_page.doc_title(title_name), 'Требуемый заголовок не найден'


def test_open_help_faq(app: ApplicationManager):
    title_name = "FAQ"
    app.help_page.faq_link_click()

    assert app.help_page.doc_title(title_name), 'Требуемый заголовок страницы не найден'


def test_open_help_consumer(app: ApplicationManager):
    title_name = "Потребителю"
    app.help_page.consumer_link_click()

    assert app.help_page.doc_title(title_name), 'Тербуемый заголовок страницы не найден'


def test_open_help_api_settings(app: ApplicationManager):
    title_name = "Настройки сервиса вызова API"
    app.help_page.consumer_link_click().api_settings_link_click()

    assert app.help_page.doc_title(title_name), 'Требуемый заголовок страницы не найден'


def test_open_help_oidc(app: ApplicationManager):
    title_name = "Токен OIDC"
    (
        app.help_page
            .consumer_link_click()
            .api_settings_link_click()
            .open_help_oidc()
    )

    assert app.help_page.doc_title(title_name), 'Требуемый заголовок страницы не найден'


def test_open_help_oauth(app: ApplicationManager):
    title_name = "Токен OAUTH"
    (
        app.help_page
            .consumer_link_click()
            .api_settings_link_click()
            .open_help_oauth()
    )

    assert app.help_page.doc_title(title_name), 'Требуемый заголовок страницы не найден'


def test_open_help_create_subscription(app: ApplicationManager):
    title_name = "Создать подписку"
    app.help_page.consumer_link_click().create_subscription_link_click()

    assert app.help_page.doc_title(title_name), 'Требуемый заголовок страницы не найден'


def test_open_help_create_certificate(app: ApplicationManager):
    title_name = "Выпустить сертификат"
    app.help_page.consumer_link_click().create_certificate_link_click()

    assert app.help_page.doc_title(title_name), 'Требуемый заголовок страницы не найден'


def test_open_help_create_app(app: ApplicationManager):
    title_name = "Зарегистрировать приложение"
    app.help_page.consumer_link_click().create_app_link_click()

    assert app.help_page.doc_title(title_name), 'Требуемый заголовок страницы не найден'


def test_open_help_provider(app: ApplicationManager):
    title_name = "Поставщику"
    app.help_page.provider_link_click()

    assert app.help_page.doc_title(title_name), 'Требуемый заголовок страницы не найден'


def test_open_help_create_agreement(app: ApplicationManager):
    title_name = "Подключить потребителя"
    app.help_page.provider_link_click()
    app.help_page.create_agreement_link_click()

    assert app.help_page.doc_title(title_name), 'Требуемый заголовок страницы не найден'

def test_open_help_create_api(app: ApplicationManager):
    title_name = "Загрузить описание API"
    app.help_page.provider_link_click()
    app.help_page.create_api_link_click()

    assert app.help_page.doc_title(title_name), 'Требуемый заголовок страницы не найден'


def test_open_help_moderation(app: ApplicationManager):
    title_name = "Критерии модерации"
    app.help_page.provider_link_click()
    app.help_page.moderation_link_click()

    assert app.help_page.doc_title(title_name), 'Требуемый заголовок страницы не найден'


def test_open_help_create_product(app: ApplicationManager):
    title_name = "Создать продукт"
    app.help_page.provider_link_click()
    app.help_page.create_product_link_click()

    assert app.help_page.doc_title(title_name), 'Требуемый заголовок страницы не найден'


def test_open_help_api_agreement(app: ApplicationManager):
    title_name = "Договор на публикацию API"
    app.help_page.provider_link_click()
    app.help_page.api_agreement_link_click()

    assert app.help_page.doc_title(title_name), 'Требуемый заголовок страницы не найден'


def test_open_help_registration(app: ApplicationManager):
    title_name = "Регистрация и вход"
    app.help_page.registration_link_click()

    assert app.help_page.doc_title(title_name), 'Требуемый заголовок страницы не найден'


def test_open_help_sberbusiness_id(app: ApplicationManager):
    title_name = "Войти по СберБизнес ID"
    app.help_page.registration_link_click()
    app.help_page.sberbusiness_id_link_click()

    assert app.help_page.doc_title(title_name), 'Требуемый заголовок страницы не найден'


def test_open_help_login(app: ApplicationManager):
    title_name = "Регистрация и вход по email"
    app.help_page.registration_link_click()
    app.help_page.login_link_click()

    assert app.help_page.doc_title(title_name), 'Требуемый заголовок страницы не найден'
