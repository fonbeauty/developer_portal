from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from model.components.base_driver import BaseDriver
from model.data_model.config import StandConfig


class Main(BaseDriver):

    _page_url = 'base_url'

    _LOGIN_LINK = '#edit-openid-connect-client-keycloak-login'
    _PROFILE_LINK = '.profile__link'
    _CATALOG_LINK = 'a[href="/catalog"]'
    _SPACE_LINK_ORG = '.currentOrg__name a'
    _USER_MENU_BLOCK = '#user_menu_block .dropdown__orgMenu.orgMenu'
    _HELP_HEADER_LINK = '.header__dropdown--element.text-link'
    _HELP_FOOTER_LINK = 'a[href$="/how-to-use"].footer__navigation-item'
    _COOKIE_BTN = '.cookie__btn .btn'

    def __init__(self, driver: WebDriver, config: StandConfig):
        self._page_url = config.urls.base_url
        super().__init__(driver)

    def set_cookie(self, cookie: dict):
        self.driver.add_cookie(cookie)

    def login_link_click(self) -> None:
        return self.wait_element(self._LOGIN_LINK).click()

    def profile_link(self) -> WebElement:
        return self.wait_element(self._PROFILE_LINK)

    def profile_link_text(self) -> str:
        return self.profile_link().text

    def open_catalog(self) -> None:
        self.wait_element(self._CATALOG_LINK).click()

    def open_user_menu(self):
        self.profile_link().click()
        self.wait_element(self._USER_MENU_BLOCK)
        return self

    def open_organization(self):
        self.wait_element(self._SPACE_LINK_ORG).click()
        return self

    def help_header_link_click(self):
        self.wait_element(self._HELP_HEADER_LINK).click()

    def help_footer_link_click(self):
        self.wait_element(self._HELP_FOOTER_LINK).click()

    def cookie_informing_close(self):
        return self.wait_element(self._COOKIE_BTN, timeout=3).click()
