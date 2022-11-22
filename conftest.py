import pytest

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from utils.load_config_data import get_config
from model.application_manager import ApplicationManager
from model.models import StandConfig
from utils import file
from utils.file import path_for_resources

CONFIG: StandConfig
DEVELOPER_COOKIE: dict


def pytest_addoption(parser):
    parser.addoption(
        '--browser',
        default='chrome',
        help='browser to run tests',
        choices=('chrome', 'safari')
    )
    parser.addoption(
        '--headless',
        action='store_true',
        help='if --headless, chrome start in headless mode',
    )
    parser.addoption(
        '--stand',
        help='stand to run tests'
    )
    pass


def pytest_sessionstart(session: pytest.Session):
    global CONFIG
    stand = session.config.getoption('--stand')
    CONFIG = get_config(stand)
    global DEVELOPER_COOKIE
    DEVELOPER_COOKIE = None
    pass


def pytest_configure(config):
    config


@pytest.fixture(scope='function')
def driver(request) -> WebDriver:
    selected_browser = request.config.getoption('--browser')
    headless = request.config.getoption('--headless')
    if selected_browser == 'chrome':
        options = webdriver.ChromeOptions()
        if headless:
            options.headless = True
        options.accept_insecure_certs = True
        options.page_load_strategy = 'normal'
        prefs = {'download.default_directory': path_for_resources()}
        options.add_experimental_option("prefs", prefs)
        _driver = webdriver.Chrome(
            executable_path='/Users/18980620/.wdm/drivers/chromedriver/mac64/104.0.5112.79/chromedriver',
            options=options
        )
    elif selected_browser == 'safari':
        _driver = webdriver.Safari()

    yield _driver

    _driver.close()


@pytest.fixture(scope='function')
def driver_developer_cookie(driver: WebDriver) -> dict:
    global DEVELOPER_COOKIE
    DEVELOPER_COOKIE = file.cookie_read()
    if DEVELOPER_COOKIE is None or file.cookie_expired(CONFIG.cookie_expire):
        developer = CONFIG.developer
        driver.get(url=CONFIG.base_url)
        wait_element(selector='#edit-openid-connect-client-keycloak-login', driver=driver).click()
        # time.sleep(3)
        wait_element(selector='#username', driver=driver).send_keys(developer.login)
        wait_element(selector='#password', driver=driver).send_keys(developer.password)
        wait_element(selector='#kc-login', driver=driver).click()
        DEVELOPER_COOKIE = driver.get_cookie(developer.session)
        file.cookie_write(DEVELOPER_COOKIE)
        return DEVELOPER_COOKIE
    else:
        return DEVELOPER_COOKIE


@pytest.fixture(scope='function')
def app(driver: WebDriver, driver_developer_cookie: dict) -> ApplicationManager:
    _app = ApplicationManager(driver)
    _app.main_page.driver.get(url='https://api.developer.sber.ru/')
    _app.main_page.driver.add_cookie(driver_developer_cookie)
    _app.main_page.driver.get(url='https://api.developer.sber.ru/')
    return _app


def wait_element(selector, driver: WebDriver, timeout=1, by=By.CSS_SELECTOR) -> WebElement:
    try:
        lolo = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((by, selector)))
        return lolo
    except TimeoutException:
        # driver.save_screenshot(f'{driver.session_id}.png')
        raise AssertionError(f'Не дождался видимости элемента {selector}')


if __name__ == '__main__':
    print(__name__)
