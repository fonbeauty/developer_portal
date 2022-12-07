from selenium.webdriver.chrome.webdriver import WebDriver

from model.components.application import Application
from model.components.applications import Applications
from model.components.catalog import Catalog
from model.components.main import Main
from model.components.product import Product
from model.components.swagger import Swagger


class ApplicationManager:

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.main_page = Main(driver)
        self.catalog = Catalog(driver)
        self.product = Product(driver)
        self.swagger = Swagger(driver)
        self.applications = Applications(driver)
        self.application = Application(driver)
