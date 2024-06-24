from typing import Tuple, List
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import allure


class UserProfile:

    def __init__(self, driver: WebDriver):
        self._driver = driver
        self._driver.get("https://www.kinopoisk.ru")
        self._driver.implicitly_wait(4)
        self._driver.maximize_window()
