import time

from selenium import webdriver


def test_hello_selenium(browser):
    browser.get(url='https://api.developer.sber.ru')
    time.sleep(1)
