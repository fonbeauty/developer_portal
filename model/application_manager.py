from selenium.webdriver.chrome.webdriver import WebDriver

from model.components.catalog import Catalog
from model.components.main import Main


class ApplicationManager:

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.main_page = Main(driver)
        self.catalog = Catalog(driver)
