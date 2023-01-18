import logging
import pytest

from pydantic import ValidationError
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.remote_connection import RemoteConnection
from requests.exceptions import HTTPError

from common import admin_api
from model.components.login import Login
from model.components.main import Main
from utils.load_config_data import get_config
from model.application_manager import ApplicationManager
from model.models import StandConfig
from utils import file
from utils.file import path_for_resources

CONFIG: StandConfig
LOGGER = logging.getLogger(__name__)


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
    try:
        CONFIG = get_config(stand)
    except ValidationError:
        msg = 'Не удалось загрузить конфиг, выполнение тестов прервано'
        LOGGER.exception(msg)
        pytest.exit(msg=msg, returncode=7)
    else:
        LOGGER.info(f'Конфигурация стенда {stand} успешно загружена')
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
    remote = request.config.getoption('--remote')
    if selected_browser == 'chrome':
        options = webdriver.ChromeOptions()
        options.accept_insecure_certs = True
        options.page_load_strategy = 'normal'
        if remote:
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
            LOGGER.info('Удаленный запуск в Moon')
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
            LOGGER.info(f'Локальный запуск, headless={headless}')
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
        LOGGER.info('Срок действия cookie админа истек или отсутствует файл с cookie')
        try:
            admin_cookie = admin_api.get_admin_cookie(CONFIG)
        except (HTTPError, AssertionError):
            pytest.exit('Ошибка логина администратором. Выполнение тестов прекращено', returncode=7)
        else:
            file.cookie_write(stand, admin.login, admin_cookie)
            LOGGER.info('Cookie админа успешно обновлена')
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


if __name__ == '__main__':
    print(__name__)
