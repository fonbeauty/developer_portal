import pytest

from conftest import CONFIG
from model.application_manager import ApplicationManager


@pytest.fixture(scope='function')
def open_main_page(authorization: ApplicationManager) -> ApplicationManager:
    authorization.main_page.driver.get(url=CONFIG.base_url)
    return authorization


def test_open_main_page(open_main_page: ApplicationManager):
    assert open_main_page.main_page.profile_link_text() == CONFIG.developer.login, 'Ссылка профиля не найдена'
    pass


def test_open_organization(open_main_page: ApplicationManager):
    link = open_main_page.main_page.organization_link()
    # open_main_page.main_page.open_organization()
    (
        open_main_page.main_page
        .open_user_menu()
        .open_organization()
    )

    assert open_main_page.applications.title_type(), 'Страница приложений загрузилась не верно'

    pass


def test_open_catalog(open_main_page: ApplicationManager):

    open_main_page.main_page.open_catalog()

    assert open_main_page.catalog.current_url() == f'{CONFIG.base_url}/catalog'
    assert open_main_page.catalog.title_text() == 'Каталог сервисов'
    assert open_main_page.catalog.count_cards() >= 16, 'Не все карточки продуктов отобразились в каталоге'
    pass


def test_search_services(open_main_page: ApplicationManager):

    open_main_page.main_page.open_catalog()
    random_product = open_main_page.catalog.random_product_card()

    product_title = open_main_page.catalog.product_title(random_product)

    open_main_page.catalog.search_product(product_title)

    found_cards = open_main_page.catalog.all_cards()

    for card in found_cards:
        assert product_title in open_main_page.catalog.product_title(card),\
            f'Поиск отработал не верно, найдена карточка без поисковой фразы "{product_title}"'
    pass


def test_open_product(open_main_page: ApplicationManager):

    open_main_page.main_page.open_catalog()
    product = open_main_page.catalog.random_product_card()
    product_title = open_main_page.catalog.product_title(product)
    open_main_page.catalog.go_to_product(product)

    pass

    assert open_main_page.product.product_title().text == product_title, 'Не найдена элемент описания сервиса'
    assert open_main_page.product.section_card(), 'Не найден элемент с условиями сервиса'


def test_open_swagger(open_main_page: ApplicationManager):

    open_main_page.main_page.open_catalog()
    product = open_main_page.catalog.random_product_card()
    open_main_page.catalog.go_to_product(product)
    open_main_page.product.go_to_token_swagger()

    pass

    assert open_main_page.swagger.title_section()
    assert open_main_page.swagger.servers_section()
    assert open_main_page.swagger.operation_section()
    assert open_main_page.swagger.schemas_section()


def test_download_swagger(open_main_page: ApplicationManager):

    open_main_page.main_page.open_catalog()
    product = open_main_page.catalog.random_product_card()
    open_main_page.catalog.go_to_product(product)
    open_main_page.product.go_to_token_swagger()
    open_main_page.swagger.download_swagger()

    pass

    assert open_main_page.swagger.title_section()
    assert open_main_page.swagger.servers_section()
    assert open_main_page.swagger.operation_section()
    assert open_main_page.swagger.schemas_section()











