from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from model.components.base_driver import BaseDriver


class Profile(BaseDriver):

    _TITLE_TYPE = '.title__type'
    _CREATE_APPLICATION_BTN = '.btn__secondary'

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def title_type(self) -> WebElement:
        return self.wait_element(self._TITLE_TYPE)

    def go_to_create_application(self) -> None:
        self.wait_element(self._CREATE_APPLICATION_BTN).click()







