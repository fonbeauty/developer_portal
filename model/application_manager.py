from selenium.webdriver.chrome.webdriver import WebDriver

from model.components.application_page import ApplicationPage
from model.components.create_application import CreateApplication
from model.components.edit_application import EditApplication
from model.components.profile import Profile
from model.components.catalog import Catalog
from model.components.how_to_use import HowToUse
from model.components.main import Main
from model.components.product import Product
from model.components.swagger import Swagger
from model.models import StandConfig
from model.components.app_keys_page import AppKeysPage
from model.components.app_revoke_certificate import AppRevokeCertificate


class ApplicationManager:

    def __init__(self, driver: WebDriver, config: StandConfig):
        self.driver = driver
        self.main_page = Main(driver, config)
        self.catalog = Catalog(driver)
        self.product = Product(driver)
        self.swagger = Swagger(driver)
        self.profile = Profile(driver, config)
        self.create_application = CreateApplication(driver, config)
        self.help_page = HowToUse(driver, config)
        self.application_page = ApplicationPage(driver, config)
        self.edit_application = EditApplication(driver, config)
        self.app_keys_page = AppKeysPage(driver, config)
        self.app_revoke_certificate = AppRevokeCertificate(driver, config)
