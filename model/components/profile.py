from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from model.components.base_driver import BaseDriver
from model.models import StandConfig


class Profile(BaseDriver):

    _PAGE_PATH = 'base_url/profile/space'
    _TITLE_TYPE = '.title__type'
    _CREATE_APPLICATION_BTN = '.btn__secondary'

    def __init__(self, driver: WebDriver, config: StandConfig):
        self.page_url = f'{config.urls.base_url}/profile/{config.users.developer.space}'
        super().__init__(driver)

    def title_type(self) -> WebElement:
        return self.wait_element(self._TITLE_TYPE)

    def open_create_application(self) -> None:
        self.wait_element(self._CREATE_APPLICATION_BTN).click()







