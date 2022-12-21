import uuid

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from model.components.base_driver import BaseDriver
from model.models import StandConfig


class CreateApplication(BaseDriver):

    _page_url = 'base_url/profile/space/app/create'

    _APP_NAME = '#edit-app-name'
    _APP_DESCRIPTION = '#edit-app-description'
    _REDIRECT_URI = '#edit-item-0'
    _PASSWORD = '#profile-settings-curr-pass'
    _PASSWORD_CONFIRMATION = '#profile-settings-new-pass-conf'
    _CANCEL_BTN = '#edit-cancel'
    _SUBMIT_BTN = '#edit-save'
    _RETURN_LINK = '.sideNav__link'
    _SUCCESS_CREATE_TEXT = '.alert.title-alert.success'
    _TO_APPLICATION_BTN = '.return-btn'
    _CLIENT_ID = '#clientId_key'
    _CLIENT_SECRET = '#clientSecretGetNew__key'
    _DOWNLOAD_CERT = '[name=download_cert]'

    def __init__(self, driver: WebDriver, config: StandConfig):
        self._page_url = f'{config.urls.base_url}/profile/{config.users.developer.space}/app/create'
        super().__init__(driver)

    def cancel_btn_click(self):
        self.wait_element(self._CANCEL_BTN).click()

    def return_link_click(self):
        self.wait_element(self._RETURN_LINK).click()

    def type_application_name(self, name: str):
        self.wait_element(self._APP_NAME).send_keys(name)
        return self

    def type_application_description(self, description: str):
        self.wait_element(self._APP_DESCRIPTION).send_keys(description)
        return self

    def type_password(self, password: str):
        self.wait_element(self._PASSWORD).send_keys(password)
        return self

    def type_password_confirmation(self, password: str):
        self.wait_element(self._PASSWORD_CONFIRMATION).send_keys(password)
        return self

    def fill_form(self,
                  password: str,
                  name: str = f'autotest_{uuid.uuid4()}',
                  description: str = 'Application was created by autotests, it should be deleted'):
        (
            self.type_application_name(name)
                .type_application_description(description)
                .type_password(password)
                .type_password_confirmation(password)
        )
        return self

    def submit(self):
        self.wait_element(self._SUBMIT_BTN).click()

    def success_create_text(self) -> WebElement:
        return self.wait_element(self._SUCCESS_CREATE_TEXT)

    def get_created_application_href(self) -> str:
        return self.wait_element(self._TO_APPLICATION_BTN).get_attribute('href')

    def client_id(self) -> str:
        return self.wait_element(self._CLIENT_ID).text

    def client_secret(self) -> str:
        return self.wait_element(self._CLIENT_SECRET).text

    def download_cert_btn(self) -> WebElement:
        return self.wait_element(self._DOWNLOAD_CERT)

    def download_cert(self) -> None:
        self.download_cert_btn().click()

