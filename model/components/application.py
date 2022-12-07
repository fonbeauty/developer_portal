import uuid

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from model.components.base_driver import BaseDriver


class Application(BaseDriver):

    _PAGE_PATH = 'profile/space/app/create'
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

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def cancel_btn_click(self):
        self.wait_element(self._CANCEL_BTN).click()

    def return_link_click(self):
        self.wait_element(self._RETURN_LINK).click()

    def type_application_name(self, name: str):
        self.wait_element(self._APP_NAME).send_keys(name)
        return self

    def type_application_description(self):
        self.wait_element(self._APP_DESCRIPTION)\
            .send_keys('Application was created by autotests, it should be deleted')
        return self

    def type_password(self, password: str):
        self.wait_element(self._PASSWORD).send_keys(password)
        return self

    def type_password_confirmation(self, password: str):
        self.wait_element(self._PASSWORD_CONFIRMATION).send_keys(password)
        return self

    def fill_form(self, password: str):
        (
            self.type_application_name(f'autotest_{uuid.uuid4()}')
                .type_application_description()
                .type_password(password)
                .type_password_confirmation(password)
        )
        return self

    def submit(self):
        self.wait_element(self._SUBMIT_BTN).click()

    def success_create_text(self) -> WebElement:
        return self.wait_element(self._SUCCESS_CREATE_TEXT)

    def to_application_btn(self) -> WebElement:
        return self.wait_element(self._TO_APPLICATION_BTN)

    def get_created_application_href(self) -> str:
        return self.to_application_btn().get_attribute('href')


