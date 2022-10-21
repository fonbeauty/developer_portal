import time

from selenium.common import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def test_hello_selenium(browser):
    browser.get(url='https://api.developer.sber.ru')
    element = browser.find_element(By.CSS_SELECTOR, '.btn.btn-blue')
    element.click()

    element_new = browser.find_element(By.CSS_SELECTOR, '#kc-login')
    assert element_new.is_displayed()
    time.sleep(1)


# def test_


def wait_element(selector, driver: WebDriver, timeout=1, by=By.CSS_SELECTOR):
    try:
        return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(by, selector))
    except TimeoutException:
        driver.save_screenshot(f'{driver.session_id}.png')
        raise AssertionError(f'Не дождался видимости элемента {selector}')
