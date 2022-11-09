from conftest import CONFIG
from model.application_manager import ApplicationManager


def test_open_main_page(app: ApplicationManager):

    assert app.main_page.profile_link_text() == 'forportal1@mail.ru', 'Ссылка профиля не найдена'


def test_go_to_catalog(app: ApplicationManager):

    app.main_page.open_catalog()

    assert app.catalog.driver.current_url == f'{CONFIG.base_url}/catalog'
    assert app.catalog.title_text() == 'Каталог сервисов'
    assert app.catalog.count_cards() <= 16, 'Не все картоки продуктов отобразились в каталоге'
    pass


def test_search_services(app: ApplicationManager):

    app.main_page.open_catalog()
    app.catalog.search_input_type_text('курсы валют')

    # time.sleep(5)

