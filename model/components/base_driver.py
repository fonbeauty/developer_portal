from selenium.common import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BaseDriver:

    _page_url: str

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def open(self):
        self.driver.get(self._page_url)
        return self

    def wait_element(self, selector, timeout=1, by=By.CSS_SELECTOR) -> WebElement:
        try:
            return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((by, selector)))
        except TimeoutException:
            pass
            # self.driver.save_screenshot(f'{self.driver.session_id}.png')
            # raise AssertionError(f'Не дождался видимости элемента {selector}')

    def wait_elements(self, selector, timeout=1, by=By.CSS_SELECTOR) -> list:
        try:
            return WebDriverWait(self.driver, timeout).until(EC.visibility_of_all_elements_located((by, selector)))
        except TimeoutException:
            pass
            # self.driver.save_screenshot(f'{self.driver.session_id}.png')
            # raise AssertionError(f'Не дождался видимости элемента {selector}')

    def current_url(self) -> str:
        return self.driver.current_url

    def waite_elements_by_xpath(self, selector, timeout=1, by=By.XPATH) -> WebElement:
        try:
            return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((by,selector)))
        except TimeoutException:
            pass