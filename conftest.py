import logging
import pytest

from pydantic import ValidationError
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.remote_connection import RemoteConnection
from requests.exceptions import HTTPError
from datetime import datetime

from common import admin_api
from model.components.login import Login
from model.components.main import Main
from utils import load_data
from model.application_manager import ApplicationManager
from model.data_model.config import StandConfig
from model.data_model.test_data import TestData
from utils import file
from utils.file import path_for_resources

CONFIG: StandConfig
TEST_DATA: TestData
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
    global TEST_DATA
    stand = session.config.getoption('--stand')
    try:
        CONFIG = load_data.get_config(stand)
    except ValidationError:
        msg = 'Не удалось загрузить конфиг, выполнение тестов прервано'
        LOGGER.exception(msg)
        pytest.exit(msg=msg, returncode=7)
    else:
        LOGGER.info(f'Конфигурация стенда {stand} успешно загружена')

    try:
        TEST_DATA = load_data.get_test_data(stand)
    except ValidationError:
        msg = 'Не удалось загрузить тестовые данные, выполнение тестов прервано'
        LOGGER.exception(msg)
        pytest.exit(msg=msg, returncode=7)
    else:
        LOGGER.info(f'Тестовые данные для стенда {stand} успешно загружена')
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
    if len(admin.cookie) == 0 or file.is_cookie_expired(stand, admin, CONFIG.timeouts.cookie_expire):
        LOGGER.info('Срок действия cookie админа истек или отсутствует файл с cookie')
        try:
            admin.cookie = admin_api.get_admin_cookie(CONFIG)
        except (HTTPError, AssertionError):
            pytest.exit('Ошибка логина администратором. Выполнение тестов прекращено', returncode=7)
        else:
            admin.cookie['creation_time'] = str(datetime.now())
            LOGGER.info('Cookie админа успешно обновлена')
    return admin.cookie


@pytest.fixture(scope='function')
def driver_cookie(driver: WebDriver) -> dict:
    stand = CONFIG.stand
    developer = CONFIG.users.developer
    if len(developer.cookie) == 0 or file.is_cookie_expired(stand, developer, CONFIG.timeouts.cookie_expire):
        LOGGER.info('Срок действия cookie пользователя истек или отсутствует файл cookie')
        try:
            Main(driver, CONFIG).open().login_link_click()
            if stand == 'dev':
                login_form = Login(driver, CONFIG)
                CONFIG.users.developer.login = login_form.get_user_login_from_label()
                login_form.do_login_user1_dev_stand()
                CONFIG.users.developer.space = login_form.get_user_space_from_url()
                pass
            else:
                Login(driver, CONFIG).login_user(login=developer.login, password=developer.password)
            if Main(driver, CONFIG).open().profile_link_text() != CONFIG.users.developer.login:
                raise AssertionError('Ошибка логина пользователя')
        except AssertionError:
            msg = 'Пользователю не удалось залогиниться. Выполнение тестов прекращено'
            LOGGER.exception(f'{msg}')
            pytest.exit(msg, returncode=7)
        except Exception as e:
            msg = 'Непредвиденное исключение при логине пользователя. Выполнение тестов прекращено'
            LOGGER.exception(f'{msg}: {e}')
            pytest.exit(msg, returncode=7)
        else:
            developer.cookie = driver.get_cookies()[0]
            developer.cookie['creation_time'] = str(datetime.now())
            LOGGER.info('Cookie пользователя успешно обновлена')
    return developer.cookie


@pytest.fixture(scope='function')
def authorization(admin_cookie: dict, driver: WebDriver, driver_cookie: dict) -> ApplicationManager:
    _app = ApplicationManager(driver, CONFIG)
    _app.main_page.open()
    _app.main_page.cookie_informing_close()
    _app.main_page.set_cookie(driver_cookie)
    return _app


if __name__ == '__main__':
    print(__name__)
