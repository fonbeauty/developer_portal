from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from model.components.base_driver import BaseDriver


class Main(BaseDriver):

    PROFILE_LINK = '.profile__link'
    CATALOG_LINK = 'a[href="/catalog"].text-link'

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def profile_link(self) -> WebElement:
        return self.wait_element(self.PROFILE_LINK)

    def profile_link_text(self) -> str:
        return self.profile_link().text

    def catalog_link(self) -> WebElement:
        return self.wait_element(self.CATALOG_LINK)

    def catalog_link_click(self) -> None:
        self.catalog_link().click()

    def open_catalog(self) -> None:
        self.catalog_link_click()
