from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from model.components.base_driver import BaseDriver


class Swagger(BaseDriver):

    TITLE_SECTION = '.title'
    SERVERS_SECTION = '.servers'
    OPERATION_SECTION = '.opblock-tag-section'
    SCHEMAS_SECTION = '.models-control'
    DOWNLOAD_SWAGGER = '#edit-download'

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def title_section(self) -> WebElement:
        return self.wait_element(self.TITLE_SECTION)

    def servers_section(self) -> WebElement:
        return self.wait_element(self.SERVERS_SECTION)

    def operation_section(self) -> WebElement:
        return self.wait_element(self.OPERATION_SECTION)

    def schemas_section(self) -> WebElement:
        return self.wait_element(self.SCHEMAS_SECTION)

    def _download_swagger_button(self) -> WebElement:
        return self.wait_element(self.DOWNLOAD_SWAGGER)

    def download_swagger(self) -> None:
        self._download_swagger_button().click()


