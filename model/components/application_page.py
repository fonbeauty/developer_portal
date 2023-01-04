import time

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from model.components.base_driver import BaseDriver
from model.models import StandConfig


class ApplcationPage(BaseDriver):

    _page_url = 'base_url/profile/space/app/application_id'

    _CLOSE_COOKIE_BTN = '.cookie__button-text'

    def __init__(self, driver: WebDriver, config: StandConfig):
        self._page_url = f'{config.urls.base_url}/profile/{config.users.developer.space}/app/create'
        super().__init__(driver)

    def edit_application(self) -> None:
        self.driver.execute_script(
            'document.getElementsByClassName("cookie__button-text")[0].style["display"] = "block"'
        )
        self.wait_element(self._CLOSE_COOKIE_BTN, timeout=2).click()
        self.wait_element(f'a[href^="{self.current_url()}"]').click()
        pass