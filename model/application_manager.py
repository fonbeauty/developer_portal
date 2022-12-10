from selenium.webdriver.chrome.webdriver import WebDriver

from model.components.application_create import ApplicationCreate
from model.components.profile import Profile
from model.components.catalog import Catalog
from model.components.main import Main
from model.components.product import Product
from model.components.swagger import Swagger
from model.models import StandConfig


class ApplicationManager:

    def __init__(self, driver: WebDriver, config: StandConfig):
        self.driver = driver
        self.main_page = Main(driver, config)
        self.catalog = Catalog(driver)
        self.product = Product(driver)
        self.swagger = Swagger(driver)
        self.profile = Profile(driver, config)
        self.application_create = ApplicationCreate(driver, config)
