from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from common.application import Application
from model.components.base_driver import BaseDriver
from model.models import StandConfig


class Profile(BaseDriver):

    _page_url = 'base_url/profile/space'

    _TITLE_TYPE = '.title__type'
    _CREATE_APPLICATION_BTN = '.btn__secondary'
    _APPLICATION_CARD = 'a[href="https://10.36.133.96:2100/profile/' \
                        '00000009-0001-0000-6787-000000000002/app/00000001-0002-0000-6787-000000000010"]'

    def __init__(self, driver: WebDriver, config: StandConfig):
        self._page_url = f'{config.urls.base_url}/profile/{config.users.developer.space}'
        super().__init__(driver)

    def title_type(self) -> WebElement:
        return self.wait_element(self._TITLE_TYPE)

    def open_create_application(self) -> None:
        self.wait_element(self._CREATE_APPLICATION_BTN).click()

    def apllication_card(self, href: str) -> WebElement:
        return self.wait_element(f'a[href="{href}"]')

    def go_to_application(self, app_instance: Application) -> None:
        self.apllication_card(app_instance.app_href).click()









