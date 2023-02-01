from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from model.components.base_driver import BaseDriver
from model.models import StandConfig


class AppCertificate(BaseDriver):
    _page_url = 'base_url/profile/space/app/app_id/certs'

    _REVOKE_CERT = '.action__revoke > a'
    _ANOTHER_REASON_RADIO_BTN = 'div:nth-child(3) > .radioBtn-checkmark'
    _PASSWORD = '#profile-settings-curr-pass'
    _PASSWORD_CONFIRMATION = '#profile-settings-new-pass-conf'
    _SUBMIT_REVOKE = '.form-submit'
    _NEW_CERT_BTN = '.btn__secondary-sm'
    _DOWNLOAD_CERT = '[name=download_cert]'
    _SUBMIT_BTN = '#edit-save'
    _SUCCESS_TEXT_PANEL = '.alert'
    _CERT_ID = '.certificatesItem:not(.certificatesItem-notValid) .certificatesItem__title'
    _CERT_ITEM_BODY = '.certificatesItem__body'

    def __init__(self, driver: WebDriver, config: StandConfig):
        self._page_url = ''
        self.config = config
        super().__init__(driver)

    def get_cert_id(self) -> str:
        return self.wait_element(self._CERT_ID).text

    def revoke_certificate_click(self) -> None:
        self.wait_element(self._REVOKE_CERT).click()

    def select_another_reason_revoke_sert(self) -> None:
        self.wait_element(self._ANOTHER_REASON_RADIO_BTN).click()

    def submit_revoke(self) -> None:
        self.wait_element(self._SUBMIT_REVOKE).click()

    def issue_new_certificate_click(self) -> None:
        self.wait_element(self._NEW_CERT_BTN).click()

    def type_password(self, password: str):
        self.wait_element(self._PASSWORD).send_keys(password)
        return self

    def type_password_confirmation(self, password: str):
        self.wait_element(self._PASSWORD_CONFIRMATION).send_keys(password)
        return self

    def type_defaults_password(self):
        (
            self.type_password(self.config.defaults.password)
                .type_password_confirmation(self.config.defaults.password)
        )
        return self

    def download_cert_btn(self) -> WebElement:
        return self.wait_element(self._DOWNLOAD_CERT)

    def submit(self) -> None:
        self.wait_element(self._SUBMIT_BTN).click()

    def success_text_panel(self) -> WebElement:
        return self.wait_element(self._SUCCESS_TEXT_PANEL)

    def is_status_cert_revoked(self, cert_id: str) -> bool:
        bodys_cert = self.wait_elements(self._CERT_ITEM_BODY)
        for item in bodys_cert:
            try:
                item_title = item.find_element(By.CSS_SELECTOR, '.certificatesItem__title').text
                item_status = item.find_element(By.CSS_SELECTOR, '.cert__status').text
            except NoSuchElementException:
                return False
            else:
                if cert_id == item_title and item_status == 'отозван':
                    return True
        return False
