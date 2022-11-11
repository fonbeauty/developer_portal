from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from model.components.base_driver import BaseDriver


class Swagger(BaseDriver):

    TITLE_SECTION = '.title'
    SERVERS_SECTION = '.servers'
    OPERATION_SECTION = '.opblock-tag-section'
    SCHEMAS_SECTION = '.models-control'

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def title_section(self) -> WebElement:
        return self.wait_element(self.TITLE_SECTION)

    def servers_section(self) -> WebElement:
        return self.wait_element(self.SERVERS_SECTION)

    def opertion_section(self) -> WebElement:
        return self.wait_element(self.OPERATION_SECTION)

    def schemas_section(self) -> WebElement:
        return self.wait_element(self.SCHEMAS_SECTION)


