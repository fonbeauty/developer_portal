from __future__ import annotations
import time
from uuid import UUID

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from model.components.base_driver import BaseDriver
from model.models import StandConfig


class AppKeysPage(BaseDriver):
    _page_url = 'base_url/profile/space/app/app_id/keys'

    _GET_NEW_CLIENT_SECRET_LINK = '.clientSecretGetNew > div.keys__btn >input'
    _GET_NEW_CLIENT_SECRET_BTN = 'div.clientSecretGetNewBtn > input.btn'
    _KEY_SHOW_BTN = 'div.actionBtn.actionBtn-show.clientSecret__key-show-btn'
    _CLIENT_SECRET = 'div.clientSecretGetNewBtn > div > input.clientSecretGetNew__key'

    def __init__(self, driver: WebDriver, config: StandConfig):
        self.name = None
        self._page_url = ''
        self.config = config
        super().__init__(driver)

    def get_new_client_secret_link_click(self) -> AppKeysPage:
        self.wait_element(self._GET_NEW_CLIENT_SECRET_LINK).click()
        return self

    def get_new_client_secret_btn_click(self) -> AppKeysPage:
        self.wait_element(self._GET_NEW_CLIENT_SECRET_BTN).click()
        return self

    def show_client_secret_btn_click(self) -> AppKeysPage:
        self.wait_element(self._KEY_SHOW_BTN).click()
        return self

    def client_secret_element(self) -> WebElement:
        return self.wait_element(self._CLIENT_SECRET)

    def client_secret(self) -> str:
        return self.client_secret_element().get_attribute('value')

    def is_valid_uuid(self, uuid_to_test, version=4) -> bool:
        try:
            UUID(uuid_to_test, version=version)
        except ValueError:
            return False
        return True

    def client_secret_input_type(self) -> str:
        return self.client_secret_element().get_attribute('type')

