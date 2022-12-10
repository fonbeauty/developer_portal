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
def driver_cookie(driver: WebDriver) -> dict:
    stand = CONFIG.stand
    user_session_id = CONFIG.users.developer.session
    global DEVELOPER_COOKIE
    DEVELOPER_COOKIE = file.cookie_read(stand, user_session_id)
    if DEVELOPER_COOKIE is None or file.cookie_expired(stand, user_session_id, CONFIG.timeouts.cookie_expire):
        developer = CONFIG.users.developer
        driver.get(url=CONFIG.urls.base_url)

        wait_element(selector='#edit-openid-connect-client-keycloak-login', driver=driver).click()
        if stand == 'dev':
            #этот локатор для дев стенда на 2001 порту:
            # wait_element(selector='label[for="edit-user-user1-3352-axvpnexamplesparta"].radioBtn-checkmark', driver=driver).click()
            #этот локатор для дев стенда на 5001 порту:
            # wait_element(selector='label[for="edit-user-user1-2273-mujiyexamplesparta"].radioBtn-checkmark', driver=driver).click()
            #этот локатор для дев стенда на 2100 порту:
            wait_element(selector='label[for="edit-user-user1-6787-zxiswexamplesparta"].radioBtn-checkmark', driver=driver).click()
            wait_element(selector='#edit-login', driver=driver).click()
        else:
            wait_element(selector='#username', driver=driver).send_keys(developer.login)
            wait_element(selector='#password', driver=driver).send_keys(developer.password)
            wait_element(selector='#kc-login', driver=driver).click()

        DEVELOPER_COOKIE = driver.get_cookie(user_session_id)
        file.cookie_write(stand, user_session_id, DEVELOPER_COOKIE)
        return DEVELOPER_COOKIE
    else:
        return DEVELOPER_COOKIE


@pytest.fixture(scope='function')
def authorization(driver: WebDriver, driver_cookie) -> ApplicationManager:
    _app = ApplicationManager(driver)
    _app.main_page.driver.get(url=CONFIG.urls.base_url)
    _app.main_page.driver.add_cookie(driver_cookie)
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
