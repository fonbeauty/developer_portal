import time

from selenium.webdriver.chrome.webdriver import WebDriver

from common.application import Application
from model.components.base_driver import BaseDriver
from model.data_model.config import StandConfig


class EditApplication(BaseDriver):

    _page_url = 'base_url/profile/space/app/application_id/edit'

    _DELETE_SUBMIT_BTN = '#edit-submit'

    def __init__(self, driver: WebDriver, config: StandConfig):
        """
        пока не понятно, как реализовать урл этой страницы
        self._page_url = f'{config.urls.base_url}/profile/{config.users.developer.space}/app/create'
        """
        self._page_url = ''
        super().__init__(driver)

    def delete_application(self, app_instance: Application) -> None:
        self.wait_element(f'a[href^="{app_instance.app_href}/delete"]').click()
        self.wait_element(self._DELETE_SUBMIT_BTN).submit()

        pass



