from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from model.components.base_driver import BaseDriver
from model.models import StandConfig


class AppCertificatePage(BaseDriver):
    _page_url = 'base_url/profile/space/app/app_id/certs'

    _REVOKE_CERT = '.cert__action.action__revoke'
    _RADIO_BTN_REVOKE_CERT = 'div:nth-child(3) > label.radioBtn-checkmark'
    _PASSWORD = '#profile-settings-curr-pass'
    _PASSWORD_CONFIRMATION = '#profile-settings-new-pass-conf'
    _EDIT_REVOKE_CERT = 'input.btn'
    _NEW_CERT_BTN = '.btn__secondary-sm'
    _DOWNLOAD_CERT = '[name=download_cert]'
    _SUBMIT_BTN = '#edit-save'
    _SUCCESS_CREATE_TEXT = 'h2.visually-hidden'

    def __init__(self, driver: WebDriver, config: StandConfig):
        self._page_url = ''
        self.config = config
        super().__init__(driver)

    def revoke_certificate_click(self) -> None:
        self.wait_element(self._REVOKE_CERT).click()

    def radio_btn_revoke_cert_click(self) -> WebElement:
        self.wait_element(self._RADIO_BTN_REVOKE_CERT).click()
        return self

    def edit_revoke_cert_click(self) -> None:
        self.wait_element(self._EDIT_REVOKE_CERT).click()

    def issue_new_certificate_click(self) -> None:
        self.wait_element(self._NEW_CERT_BTN).click()

    def type_password(self, password: str):
        self.wait_element(self._PASSWORD).send_keys(password)
        return self

    def type_password_confirmation(self, password: str):
        self.wait_element(self._PASSWORD_CONFIRMATION).send_keys(password)
        return self

    def password_form(self, password: str = None):
        (
            self.type_password(password or self.config.defaults.password)
                .type_password_confirmation(password or self.config.defaults.password)
        )
        return self

    def download_cert_btn(self) -> WebElement:
        return self.wait_element(self._DOWNLOAD_CERT)

    def submit(self) -> None:
        self.wait_element(self._SUBMIT_BTN).click()

    def success_create_text(self) -> bool:
        return True if self.wait_element(self._SUCCESS_CREATE_TEXT) else False
