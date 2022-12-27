import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from model.components.base_driver import BaseDriver

from model.models import StandConfig


class HowToUse(BaseDriver):
    _page_url = 'base_url/how-to-use/aboutx'

    _COOCKIE_BTN = 'div.cookie > div > div > div.cookie__btn > div'
    _CONTACTS_BTN = 'a.docMenu__item-link[href="/how-to-use/contacts"]'
    _HELP_TITLE = '.offer__title'
    # _CONTACTS_TITLE = "//div/h1[text()='Контакты']"
    _SEARCH_INPUT_FIELD = '.search__item-input'
    _FAQ_BTN = '[href="/how-to-use/faq"]'
    _CONSUMER_LINK = '[href="/how-to-use/consumer"]'
    _API_SETTINGS_LINK = '[href="/how-to-use/api_settings"]'
    _TOKEN_OIDC_LINK = '[href="/how-to-use/token_oidc"]'
    _TOKEN_OAUTH_LINK = '[href="/how-to-use/token_oauth"]'
    _DOC_TITLE = '.documentation__title'
    _CREATE_SUBSCRIPTION_LINK = '[href="/how-to-use/create_subscription"]'
    _CREATE_CERTIFICATE_LINK = '[href="/how-to-use/create_certificate"]'
    _CREATE_APP_LINK = '[href = "/how-to-use/create_app"]'
    _PROVIDER_LINK = '[href="/how-to-use/provider"]'
    _CREATE_AGREEMENT = '[href="/how-to-use/create_agreement"]'
    _CREATE_API = '[href="/how-to-use/create_api"]'
    _MODERATION = '[href="/how-to-use/moderation"]'
    _CREATE_PRODUCT = '[href="/how-to-use/create_product"]'
    _API_AGREEMENT = '[href="/how-to-use/api_agreement"]'
    _REGISTRATION = '[href="/how-to-use/registration"]'
    _SBERBUSINESS_ID = '[href="/how-to-use/sberbusiness_id"]'
    _LOGIN = '[href="/how-to-use/login"]'

    def __init__(self, driver: WebDriver, config: StandConfig):
        self._page_url = f'{config.urls.base_url}/how-to-use/about'
        super().__init__(driver)

    def cookie_informing_close(self):
        return self.wait_element(self._COOCKIE_BTN).click()

    def contacts_link_click(self):
        self.wait_element(self._CONTACTS_BTN).click()

    def help_title(self) -> WebElement:
        return self.wait_element(self._HELP_TITLE)

    def input_text_search_bar(self, text: str):
        search_bar = self.wait_element(self._SEARCH_INPUT_FIELD)
        search_bar.send_keys(text)
        search_bar.send_keys(Keys.RETURN)

    def faq_link_click(self):
        self.wait_element(self._FAQ_BTN).click()

    def consumer_link_click(self):
        self.wait_element(self._CONSUMER_LINK).click()
        return self

    def api_settings_link_click(self):
        self.wait_element(self._API_SETTINGS_LINK).click()
        return self

    def open_help_oidc(self):
        self.wait_element(self._TOKEN_OIDC_LINK).click()

    def open_help_oauth(self):
        self.wait_element(self._TOKEN_OAUTH_LINK).click()

    def doc_title(self, title_name: str) -> bool:
        return self.wait_element(self._DOC_TITLE).text == f"{title_name}"

    def create_subscription_link_click(self):
        self.wait_element(self._CREATE_SUBSCRIPTION_LINK).click()

    def create_certificate_link_click(self):
        self.wait_element(self._CREATE_CERTIFICATE_LINK).click()

    def create_app_link_click(self):
        self.wait_element(self._CREATE_APP_LINK).click()

    def provider_link_click(self):
        self.wait_element(self._PROVIDER_LINK).click()

    def create_agreement_link_click(self):
        self.wait_element(self._CREATE_AGREEMENT).click()

    def create_api_link_click(self):
        self.wait_element(self._CREATE_API).click()

    def moderation_link_click(self):
        self.wait_element(self._MODERATION).click()

    def create_product_link_click(self):
        self.wait_element(self._CREATE_PRODUCT).click()

    def api_agreement_link_click(self):
        self.wait_element(self._API_AGREEMENT).click()

    def registration_link_click(self):
        self.wait_element(self._REGISTRATION).click()

    def sberbusiness_id_link_click(self):
        self.wait_element(self._SBERBUSINESS_ID).click()

    def login_link_click(self):
        self.wait_element(self._LOGIN).click()