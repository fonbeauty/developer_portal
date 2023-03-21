from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from model.components.base_driver import BaseDriver


class Product(BaseDriver):

    OFFER_TEXT = '.offer__text'
    PRODUCT_TITLE = '.offer__title'
    SECTION_CARD = '.section-card'
    _TARIFF_SELECTION = '.radioBtn-checkmark'
    _BTN_NEXT = '.subsBtn-next'
    _STOP_SUBS = '.product-card__sidebar-data > a'
    TOKEN_HREF = 'a[href$="/swagger/download_token_3_0_0"]'
    # _PRODUCT = 'a[href="https://10.36.133.96:2100/profile/00000009-0001-0000-9007-000000000002/product' \
    #            '/prodCode002st9007"] '
    # _PRODUCT_SUBSCRIBE = 'a[href="/product/prodCode002st9007/subscribe"]'

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def offer_text(self) -> WebElement:
        return self.wait_element(self.OFFER_TEXT)

    def product_title(self) -> WebElement:
        return self.wait_element(self.PRODUCT_TITLE)

    def section_card(self) -> WebElement:
        return self.wait_element(self.SECTION_CARD)

    def go_to_token_swagger(self) -> None:
        self.wait_element(self.TOKEN_HREF).click()

    def stop_subs_click(self) -> None:
        self.wait_element(self._STOP_SUBS).click()

    # def go_to_product(self) -> None:
    #     self.wait_element(self._PRODUCT).click()

    # def token_href(self) -> WebElement:
    #     return self.wait_element(self.TOKEN_HREF)

    # def test_subscribe_click(self) -> None:
    #     self.wait_element(self._PRODUCT_SUBSCRIBE).click()





