from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from common.application import Application
from model.components.base_driver import BaseDriver
from model.models import StandConfig


class Profile(BaseDriver):

    _page_url = 'base_url/profile/space'

    _TITLE_TYPE = '.title__type'
    _CREATE_APPLICATION_BTN = '.btn__secondary'

    def __init__(self, driver: WebDriver, config: StandConfig):
        self._page_url = f'{config.urls.base_url}/profile/{config.users.developer.space}'
        super().__init__(driver)

    def title_type(self) -> WebElement:
        return self.wait_element(self._TITLE_TYPE)

    def open_create_application(self) -> None:
        self.wait_element(self._CREATE_APPLICATION_BTN).click()

    def go_to_application(self, app_instance: Application) -> None:
        self.wait_element(f'a[href="{app_instance.app_href}"]').click()

    def application_card_not_exist(self, app_instance: Application) -> bool:
        return not self.wait_element(f'a[href="{app_instance.app_href}"]')
