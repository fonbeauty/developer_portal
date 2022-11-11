from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from model.components.base_driver import BaseDriver


class Product(BaseDriver):

    OFFER_TEXT = '.offer__text'
    PRODUCT_TITLE = '.offer__title'
    SECTION_CARD = '.section-card'
    

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def offer_text(self) -> WebElement:
        return self.wait_element(self.OFFER_TEXT)

    def product_title(self) -> WebElement:
        return self.wait_element(self.PRODUCT_TITLE)

    def section_card(self):
        return self.wait_element(self.SECTION_CARD)



