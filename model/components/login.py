from selenium.webdriver.chrome.webdriver import WebDriver

from model.components.base_driver import BaseDriver
from model.data_model.config import StandConfig


class Login(BaseDriver):

    _page_url = 'base_url/login'

    _DEV_STAND_SELECT_USER = 'label[for^="edit-user-user1-"].radioBtn-checkmark'
    _DEV_STAND_SELECT_USER_LABEL = 'label[for^="edit-user-user1-"].radioBtnLabel'
    _DEV_STAND_LOGIN_BTN = '#edit-login'

    _USERNAME = '#username'
    _PASSWORD = '#password'
    _LOGIN_BTN = '#kc-login'

    def __init__(self, driver: WebDriver, config: StandConfig):
        super().__init__(driver)

    def get_user_login_from_label(self) -> str:
        text = self.wait_element(self._DEV_STAND_SELECT_USER_LABEL).text
        index_user_login = text.find(' ')
        user_login = text[:index_user_login]
        return user_login

    def do_login_user1_dev_stand(self):
        self.wait_element(self._DEV_STAND_SELECT_USER).click()
        self.wait_element(self._DEV_STAND_LOGIN_BTN).click()
        return self

    def get_user_space_from_url(self) -> str:
        url = self.current_url()
        index_space = url.rfind('/')+1
        return url[index_space:]

    def login_user(self, login: str, password: str) -> None:
        self.wait_element(self._USERNAME).send_keys(login)
        self.wait_element(self._PASSWORD).send_keys(password)
        self.wait_element(self._LOGIN_BTN).click()
