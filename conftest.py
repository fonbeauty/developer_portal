import pytest

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from configs.load_data import get_config


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


def pytest_sessionstart(session):
    global CONFIG
    CONFIG = get_config()
    pass


@pytest.fixture()
def browser(request) -> WebDriver:
    selected_browser = request.config.getoption('--browser')
    headless = request.config.getoption('--headless')

    if selected_browser == 'chrome':
        options = webdriver.ChromeOptions()
        if headless:
            options.headless = True
        _browser = webdriver.Chrome(
            executable_path='/Users/18980620/.wdm/drivers/chromedriver/mac64/98.0.4758.102/chromedriver',
            options=options
        )
    elif selected_browser == 'safari':
        _browser = webdriver.Safari()

    yield _browser

    _browser.close()
