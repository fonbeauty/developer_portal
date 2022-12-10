from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from model.components.base_driver import BaseDriver
from model.models import StandConfig


class Main(BaseDriver):

    _PROFILE_LINK = '.profile__link'
    _CATALOG_LINK = 'a[href="/catalog"].text-link'
    _SPACE_LINK_ORG = '.currentOrg__name a'
    _USER_MENU_BLOCK = '#user_menu_block .dropdown__orgMenu.orgMenu'

    def __init__(self, driver: WebDriver, config: StandConfig):
        self.page_url = config.urls.base_url
        super().__init__(driver)

    def set_cookie(self, cookie: dict):
        self.driver.add_cookie(cookie)

    def profile_link(self) -> WebElement:
        return self.wait_element(self._PROFILE_LINK)

    def profile_link_text(self) -> str:
        return self.profile_link().text

    def catalog_link(self) -> WebElement:
        return self.wait_element(self._CATALOG_LINK)

    def catalog_link_click(self) -> None:
        self.catalog_link().click()

    def open_catalog(self) -> None:
        self.catalog_link_click()

    def organization_link(self) -> WebElement:
        return self.wait_element(self._SPACE_LINK_ORG)

    def open_user_menu(self):
        self.profile_link().click()
        self.wait_element(self._USER_MENU_BLOCK)
        return self

    def open_organization(self):
        self.organization_link().click()
        return self

