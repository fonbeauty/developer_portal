from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from model.components.base_driver import BaseDriver


class Applications(BaseDriver):

    TITLE_TYPE = '.title__type'

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def title_type(self) -> WebElement:
        return self.wait_element(self.TITLE_TYPE)

