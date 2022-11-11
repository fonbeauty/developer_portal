import random

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from model.components.base_driver import BaseDriver


class Catalog(BaseDriver):

    CATALOG_TITLE = '.catalog__title'
    SEARCH_INPUT = '.input-search'
    CARD_RATES = 'a[href="/product/ExchangeRates"]'
    ALL_CARDS = '.card'
    GROUP_CARDS = '.catalog__cards'
    CARD_TITLE = '.card-title'

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def catalog_title(self) -> WebElement:
        return self.wait_element(self.CATALOG_TITLE)

    def title_text(self) -> str:
        return self.catalog_title().text

    def search_input(self) -> WebElement:
        return self.wait_element(self.SEARCH_INPUT)

    def search_text(self, text_for_search: str) -> None:
        self.search_input().send_keys(text_for_search)
        self.search_input().submit()

    def card_rates(self) -> WebElement:
        return self.wait_element(self.CARD_RATES)

    def open_card_rates(self) -> None:
        self.card_rates().click()

    def all_cards(self) -> list:
        return self.wait_elements(self.ALL_CARDS)

    def count_cards(self) -> int:
        return len(self.all_cards())

    def group_cards(self) -> WebElement:
        return self.wait_element(self.GROUP_CARDS)

    def product_href(self, product: WebElement) -> str:
        return product.get_attribute('href')

    def product_title(self, product: WebElement) -> str:
        return product.get_attribute('text').splitlines()[1].strip()

    def random_product_card(self) -> WebElement:
        return random.choice(self.all_cards())

    def go_to_product(self, product: WebElement) -> None:
        product.click()








