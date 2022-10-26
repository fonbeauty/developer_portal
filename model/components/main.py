from selenium.common import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Main:

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def element(self, selector, timeout=1, by=By.CSS_SELECTOR) -> WebElement:
        try:
            return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((by, selector)))
        except TimeoutException:
            self.driver.save_screenshot(f'{self.driver.session_id}.png')
            raise AssertionError(f'Не дождался видимости элемента {selector}')

    def check_email(self):
        self.element('.profile__link.opened')
        return self
