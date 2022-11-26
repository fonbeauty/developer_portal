from conftest import CONFIG
from model.application_manager import ApplicationManager


def test_open_main_page(app: ApplicationManager):
    assert app.main_page.profile_link_text() == CONFIG.developer.login, 'Ссылка профиля не найдена'


def test_open_catalog(app: ApplicationManager):

    app.main_page.open_catalog()

    assert app.catalog.current_url() == f'{CONFIG.base_url}/catalog'
    assert app.catalog.title_text() == 'Каталог сервисов'
    assert app.catalog.count_cards() >= 16, 'Не все карточки продуктов отобразились в каталоге'
    pass


def test_search_services(app: ApplicationManager):

    app.main_page.open_catalog()
    random_product = app.catalog.random_product_card()

    product_title = app.catalog.product_title(random_product)

    app.catalog.search_product(product_title)

    found_cards = app.catalog.all_cards()

    for card in found_cards:
        assert product_title in app.catalog.product_title(card),\
            f'Поиск отработал не верно, найдена карточка без поисковой фразы "{product_title}"'
    pass


def test_open_product(app: ApplicationManager):

    app.main_page.open_catalog()
    product = app.catalog.random_product_card()
    product_title = app.catalog.product_title(product)
    app.catalog.go_to_product(product)

    pass

    assert app.product.product_title().text == product_title, 'Не найдена элемент описания сервиса'
    assert app.product.section_card(), 'Не найден элемент с условиями сервиса'


def test_open_swagger(app: ApplicationManager):

    app.main_page.open_catalog()
    product = app.catalog.random_product_card()
    app.catalog.go_to_product(product)
    app.product.go_to_token_swagger()

    pass

    assert app.swagger.title_section()
    assert app.swagger.servers_section()
    assert app.swagger.operation_section()
    assert app.swagger.schemas_section()


def test_download_swagger(app: ApplicationManager):

    app.main_page.open_catalog()
    product = app.catalog.random_product_card()
    app.catalog.go_to_product(product)
    app.product.go_to_token_swagger()
    app.swagger.download_swagger()

    pass

    assert app.swagger.title_section()
    assert app.swagger.servers_section()
    assert app.swagger.operation_section()
    assert app.swagger.schemas_section()











