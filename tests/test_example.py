from conftest import CONFIG
from model.application_manager import ApplicationManager


def test_open_main_page(app: ApplicationManager):

    assert app.main_page.profile_link_text() == 'forportal1@mail.ru', 'Ссылка профиля не найдена'


def test_open_catalog(app: ApplicationManager):

    app.main_page.open_catalog()

    assert app.catalog.current_url() == f'{CONFIG.base_url}/catalog'
    assert app.catalog.title_text() == 'Каталог сервисов'
    assert app.catalog.count_cards() <= 16, 'Не все картоки продуктов отобразились в каталоге'
    pass


def test_search_services(app: ApplicationManager):

    app.main_page.open_catalog()
    app.catalog.search_text('курсы валют')

    assert app.catalog.count_cards() == 1, 'Найдено более одной карточки продуктов'
    assert app.catalog.card_rates(), 'Не найдено карточки продукта Курсы валют'
    pass


def test_open_product(app: ApplicationManager):

    app.main_page.open_catalog()
    product = app.catalog.random_product_card()
    product_href = app.catalog.product_href(product)
    product_title = app.catalog.product_title(product)
    app.catalog.go_to_product(product)

    pass

    assert app.product.current_url() == product_href, 'URL не совпадает с заданным'
    assert app.product.product_title().text == product_title, 'Не найдена элемент описания сервиса'
    assert app.product.section_card(), 'Не найден элемент с условиями сервиса'









