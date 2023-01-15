import pytest
import requests

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.remote_connection import RemoteConnection

from model.components.login import Login
from model.components.main import Main
from utils.load_config_data import get_config
from model.application_manager import ApplicationManager
from model.models import StandConfig
from utils import file
from utils.file import path_for_resources
from bs4 import BeautifulSoup

CONFIG: StandConfig


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
    parser.addoption(
        '--remote',
        action='store_true',
        help='if --remote, tests run on remote server moon',
    )
    parser.addoption(
        '--browser_version',
        default='104.0',
        help='browser version to run tests',
    )
    pass


def pytest_sessionstart(session: pytest.Session):
    global CONFIG
    stand = session.config.getoption('--stand')
    CONFIG = get_config(stand)
    pass


def pytest_configure(config):
    config


@pytest.fixture(scope='session')
def portal_session():
    pass


@pytest.fixture(scope='function')
def driver(request) -> WebDriver:
    selected_browser = request.config.getoption('--browser')
    headless = request.config.getoption('--headless')
    if selected_browser == 'chrome':
        options = webdriver.ChromeOptions()
        options.accept_insecure_certs = True
        options.page_load_strategy = 'normal'
        if request.config.getoption('--remote'):
            capabilities = {
                'browserName': 'chrome',
                'browserVersion': request.config.getoption('--browser_version'),
                'moon:options': {
                    'enableVNC': True,
                },
                'goog:chromeOptions': {
                    'args': ['no-sandbox', 'start-maximized']
                }
            }
            hub = f'http://{CONFIG.moon.user}:{CONFIG.moon.password}@{CONFIG.moon.host}/wd/hub'
            _driver = webdriver.Remote(
                command_executor=RemoteConnection(hub),
                desired_capabilities=capabilities,
                options=options
            )
            pass
        else:
            if headless:
                options.headless = True
            prefs = {'download.default_directory': path_for_resources()}
            options.add_experimental_option('prefs', prefs)
            _driver = webdriver.Chrome(
                executable_path=CONFIG.paths.chromedriver_path,
                options=options
            )
    elif selected_browser == 'safari':
        _driver = webdriver.Safari()

    yield _driver

    _driver.quit()


@pytest.fixture(scope='function')
def admin_cookie(driver: WebDriver) -> dict:
    stand = CONFIG.stand
    admin = CONFIG.users.admin
    admin_cookie = file.cookie_read(stand, admin.login)

    if admin_cookie is None or file.cookie_expired(stand, admin.login, CONFIG.timeouts.cookie_expire):
        response = requests.get(
            url=f'{CONFIG.urls.base_url}/user/login',
            verify=False
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        form_build_id = soup.select('input[name=form_build_id]')[1]['value']

        request_body = {
            'name': f'{CONFIG.users.admin.login}',
            'pass': f'{CONFIG.users.admin.password}',
            'form_build_id': f'{form_build_id}',
            'form_id': 'user_login_form',
            'op': 'Log in'
        }
        response = requests.post(
            url=f'{CONFIG.urls.base_url}/user/login',
            data=request_body,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            verify=False
        )
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        assert soup.select('#toolbar-item-user'), 'Не удалось залогиниться администратором'

        admin_cookie = dict(name=f'{response.cookies.keys()[0]}', value=f'{response.cookies.values()[0]}')

        file.cookie_write(stand, admin.login, admin_cookie)

    return admin_cookie


@pytest.fixture(scope='function')
def driver_cookie(driver: WebDriver) -> dict:
    stand = CONFIG.stand
    developer = CONFIG.users.developer
    developer_cookie = file.cookie_read(stand, developer.login)
    if developer_cookie is None or file.cookie_expired(stand, developer.login, CONFIG.timeouts.cookie_expire):
        Main(driver, CONFIG).open().login_link_click()
        if stand == 'dev':
            Login(driver, CONFIG).login_user1_dev_stand()
        else:
            Login(driver, CONFIG).login_user(login=developer.login, password=developer.password)
            # wait_element(selector='#username', driver=driver).send_keys(developer.login)
            # wait_element(selector='#password', driver=driver).send_keys(developer.password)
            # wait_element(selector='#kc-login', driver=driver).click()
        developer_cookie = driver.get_cookies()[0]
        file.cookie_write(stand, developer.login, developer_cookie)

    return developer_cookie


@pytest.fixture(scope='function')
def authorization(admin_cookie: dict, driver: WebDriver, driver_cookie: dict) -> ApplicationManager:
    _app = ApplicationManager(driver, CONFIG)
    _app.main_page.open()
    _app.main_page.cookie_informing_close()
    _app.main_page.set_cookie(driver_cookie)
    return _app


# def wait_element(selector, driver: WebDriver, timeout=1, by=By.CSS_SELECTOR) -> WebElement:
#     try:
#         lolo = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((by, selector)))
#         return lolo
#     except TimeoutException:
#         # driver.save_screenshot(f'{driver.session_id}.png')
#         raise AssertionError(f'Не дождался видимости элемента {selector}')


if __name__ == '__main__':
    print(__name__)
