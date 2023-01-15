from selenium.webdriver.chrome.webdriver import WebDriver

from model.components.base_driver import BaseDriver
from model.models import StandConfig


class Login(BaseDriver):
    _page_url = 'base_url/login'

    _DEV_STAND_SELECT_USER = 'label[for="edit-user-user1-6787-zxiswexamplesparta"].radioBtn-checkmark'
    _DEV_STAND_LOGIN_BTN = '#edit-login'

    _USERNAME = '#username'
    _PASSWORD = '#password'
    _LOGIN_BTN = '#kc-login'

    def __init__(self, driver: WebDriver, config: StandConfig):
        super().__init__(driver)

    def login_user1_dev_stand(self) -> None:
        self.wait_element(self._DEV_STAND_SELECT_USER).click()
        self.wait_element(self._DEV_STAND_LOGIN_BTN).click()

    def login_user(self, login: str, password: str) -> None:
        self.wait_element(self._USERNAME).send_keys(login)
        self.wait_element(self._PASSWORD).send_keys(password)
        self.wait_element(self._LOGIN_BTN).click()
