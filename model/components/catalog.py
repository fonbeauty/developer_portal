from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from model.components.base_driver import BaseDriver


class Catalog(BaseDriver):

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def catalog_title(self) -> WebElement:
        return self.wait_element('.catalog__title')

    def catalog_title_text(self) -> str:
        return self.catalog_title().text

    def search_input(self) -> WebElement:
        return self.wait_element('.input-search')

    def search_input_type_text(self, text_for_search: str) -> None:
        self.search_input().send_keys(text_for_search)
        self.search_input().submit()

