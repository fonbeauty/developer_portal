from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from model.components.base_driver import BaseDriver


class Applications(BaseDriver):

    TITLE_TYPE = '.title__type'
    CREATE_APPLICATION_BTN = '.btn__secondary'

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def title_type(self) -> WebElement:
        return self.wait_element(self.TITLE_TYPE)

    # def create_application_btn(self) -> WebElement:
    #     return self.wait_element(self.CREATE_APPLICATION_BTN)

    def go_to_create_application(self) -> None:
        self.wait_element(self.CREATE_APPLICATION_BTN).click()







