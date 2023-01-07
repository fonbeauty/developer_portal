import time

from selenium.webdriver.chrome.webdriver import WebDriver

from common.application import Application
from model.components.base_driver import BaseDriver
from model.models import StandConfig


class ApplicationPage(BaseDriver):
    _page_url = 'base_url/profile/space/app/application_id'

    _CLOSE_COOKIE_BTN = '.cookie__button-text'

    def __init__(self, driver: WebDriver, config: StandConfig):
        """
        пока не понятно, как реализовать урл этой страницы
        self._page_url = f'{config.urls.base_url}/profile/{config.users.developer.space}/app/create'
        """
        self._page_url = ''
        super().__init__(driver)

    def go_to_edit_application(self, app_instance: Application) -> None:
        self.driver.execute_script(
            'document.getElementsByClassName("cookie__button-text")[0].style["display"] = "block"'
        )
        self.wait_element(self._CLOSE_COOKIE_BTN, timeout=3).click()
        self.wait_element(f'a[href^="{app_instance.app_href}"]').click()
        pass
