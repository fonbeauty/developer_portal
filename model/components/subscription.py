from __future__ import annotations

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select

from common.application import Application
from model.components.base_driver import BaseDriver
from model.data_model.config import StandConfig


class Subscription(BaseDriver):
    _page_url = 'base_url/product/prodCode/subscribe'

    _CONNECT_BTN = '.btn-blue'
    _RADIO_BTN = ':nth-child(2) > .radioBtn-checkmark'
    _SUBS_BTN_NEXT = '.subsBtn-next'
    _CREATE_NEW_APP = '.radioBtnLabel[for="edit-choose-application-new"]'
    _TITLE_ALERT = '.title-alert'
    _CANCEL_BTN = '.btn-grey'
    _BACK_BTN = '.subsBtn-prev'
    _APP_LIST = '.has-value'
    _NAME_APP = ':nth-child(3) > .fieldGroup__text'
    _SUBMIT = '.form-submit'

    def __init__(self, driver: WebDriver, config: StandConfig):
        self._page_url = ''
        self.config = config
        super().__init__(driver)

    def connect_click(self):
        self.wait_element(self._CONNECT_BTN).click()
        return self

    def select_tariff_click(self):
        self.wait_element(self._RADIO_BTN).click()
        return self

    def subs_btn_next_click(self):
        self.wait_element(self._SUBS_BTN_NEXT).click()
        return self

    def create_new_app_click(self):
        self.wait_element(self._CREATE_NEW_APP).click()
        return self

    def title_alert(self) -> WebElement:
        return self.wait_element(self._TITLE_ALERT)

    def cancel_click(self):
        self.wait_element(self._CANCEL_BTN).click()
        return self

    def back_click(self):
        self.wait_element(self._BACK_BTN).click()
        return self

    def drop_down_list(self) -> WebElement:
        return self.wait_element(self._APP_LIST)

    def select_app(self, app_name: str) -> Subscription:
        drop = Select(self.drop_down_list())
        drop.select_by_visible_text(app_name)
        return self

    def get_name_app(self) -> str:
        return self.wait_element(self._NAME_APP).text

    def submit_click(self) -> None:
        self.wait_element(self._SUBMIT).click()

    def select_tariff(self) -> None:
        self.connect_click() \
            .select_tariff_click() \
            .subs_btn_next_click()
        return self

    def select_app_from_list(self, app_name=None) -> None:
        if app_name is None:
            self.create_new_app_click()
        else:
            self.select_app(app_name) \
                .subs_btn_next_click() \
                .subs_btn_next_click()
