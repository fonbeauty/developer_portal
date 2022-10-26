import time

from selenium.webdriver.chrome.webdriver import WebDriver

from conftest import CONFIG

# def test_hello_selenium(driver):
#     browser.get(url=CONFIG.base_url)
#     element = browser.find_element(By.CSS_SELECTOR, '.btn.btn-blue')
#     element.click()
#
#     element_new = browser.find_element(By.CSS_SELECTOR, '#kc-login')
#     assert element_new.is_displayed()
#     time.sleep(1)


# def test_developer_login(driver):
#     driver.get(url=CONFIG.base_url)
#     wait_element(selector='#edit-openid-connect-client-keycloak-login', driver=driver).click()
#     # time.sleep(3)
#     wait_element(selector='#username', driver=driver).send_keys(CONFIG.developer.login)
#     wait_element(selector='#password', driver=driver).send_keys(CONFIG.developer.password)
#     wait_element(selector='#kc-login', driver=driver).click()
#     global COOKIE
#     COOKIE = driver.get_cookie(CONFIG.developer.session)
#     print(COOKIE['name'])
#     print(COOKIE['value'])
#     print(COOKIE['domain'])
#     time.sleep(10)


# def test_open_base_page(driver: WebDriver, driver_developer_cookie: dict):
#     driver.get(url=CONFIG.base_url)
#     driver.add_cookie(driver_developer_cookie)
#     driver.get(url='https://api.developer.sber.ru/profile/17124919-4b8c-444d-a9d9-a062ec95bd38')
#     time.sleep(2)
from model.components.main import Main


def test_open_main_page(main_page: Main, driver_developer_cookie: dict):
    # driver.get(url=CONFIG.base_url)
    main_page.driver.add_cookie(driver_developer_cookie)
    main_page.driver.get(url='https://api.developer.sber.ru/')
    element = main_page.check_email()

    time.sleep(2)


# def test_open_base_page3(driver: WebDriver, driver_developer_cookie: dict):
#     driver.get(url=CONFIG.base_url)
#     driver.add_cookie(driver_developer_cookie)
#     driver.get(url='https://api.developer.sber.ru/profile/view')
#     time.sleep(2)
#
#
# def test_open_base_page4(driver: WebDriver, driver_developer_cookie: dict):
#     driver.get(url=CONFIG.base_url)
#     driver.add_cookie(driver_developer_cookie)
#     driver.get(url='https://api.developer.sber.ru/catalog')
#     time.sleep(2)