from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from model.components.base_driver import BaseDriver


class Main(BaseDriver):

    PROFILE_LINK = '.profile__link'
    CATALOG_LINK = 'a[href="/catalog"].text-link'
    SPACE_LINK_ORG = '.currentOrg__name a'
    USER_MENU_BLOCK = '#user_menu_block .dropdown__orgMenu.orgMenu'

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def profile_link(self) -> WebElement:
        return self.wait_element(self.PROFILE_LINK)

    def profile_link_text(self) -> str:
        return self.profile_link().text

    def catalog_link(self) -> WebElement:
        return self.wait_element(self.CATALOG_LINK)

    def catalog_link_click(self) -> None:
        self.catalog_link().click()

    def open_catalog(self) -> None:
        self.catalog_link_click()

    def organization_link(self) -> WebElement:
        return self.wait_element(self.SPACE_LINK_ORG)

    def open_user_menu(self):
        self.profile_link().click()
        self.wait_element(self.USER_MENU_BLOCK)
        return self

    def open_organization(self):
        self.organization_link().click()
        return self

