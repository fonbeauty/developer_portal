
from selenium.webdriver.chrome.webdriver import WebDriver

from common.application import Application
from model.components.base_driver import BaseDriver
from model.data_model.config import StandConfig


class ApplicationPage(BaseDriver):
    _page_url = 'base_url/profile/space/app/application_id'

    _CERTIFICATE = 'li:nth-child(3)'
    _KEYS = '#block-tabs li:nth-child(2) > a'
    _NAME_APP = '.title__value'
    _CATALOG = 'a[href="/catalog"]'


    def __init__(self, driver: WebDriver, config: StandConfig):
        """
        пока не понятно, как реализовать урл этой страницы
        self._page_url = f'{config.urls.base_url}/profile/{config.users.developer.space}/app/create'
        """
        self._page_url = ''
        super().__init__(driver)

    def go_to_edit_application(self, app_instance: Application) -> None:
        self.wait_element(f'a[href^="{app_instance.app_href}"]').click()
        pass

    def go_to_certificates(self) -> None:
        self.wait_element(self._CERTIFICATE).click()

    def go_to_keys(self) -> None:
        self.wait_element(self._KEYS).click()

    def get_name_app(self) -> str:
        return self.wait_element(self._NAME_APP).text

    def go_to_catalog(self) -> None:
        self.wait_element(self._CATALOG).click()