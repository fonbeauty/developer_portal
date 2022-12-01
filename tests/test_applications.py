import time

import pytest
from selenium.webdriver.chrome.webdriver import WebDriver

from conftest import CONFIG
from model.application_manager import ApplicationManager


@pytest.fixture(scope='function')
def open_application_page(authorization: ApplicationManager) -> ApplicationManager:
    authorization.main_page.driver.get(url=f'{CONFIG.base_url}/profile/{CONFIG.developer.space}')
    return authorization


# @pytest.mark.parametrize('app', [f'profile/{CONFIG.developer.space}'], indirect=True)
def test_create_application_test(open_application_page):
    pass
    # time.sleep(3)