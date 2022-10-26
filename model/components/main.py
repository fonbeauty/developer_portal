from selenium.common import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from model.components.base_driver import BaseDriver


class Main(BaseDriver):

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def profile_link(self) -> WebElement:
        return self.wait_element('.profile__link')

    def profile_link_text(self) -> str:
        return self.profile_link().text

    def catalog_link(self) -> WebElement:
        return self.wait_element('a[href="/catalog"].text-link')

    def catalog_link_click(self) -> None:
        self.catalog_link().click()
