from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import allure


class Auth:

    def __init__(self, driver: str):
        self._driver = driver
        self._driver.get("https://www.kinopoisk.ru")
        self._driver.implicitly_wait(4)
        self._driver.maximize_window()

    @allure.step(
        "Переходим на сайт Кинопоиск. Авторизуемся на сайте. Ожидаем возвращения на главную страницу. Логин - {login}, пароль - {password}."
    )
    def user_auth(self, login: str, password: str):
        """Данный метод позволяет пользователю авторизоваться
        на сайте, используя полученные входные данные.

        Args:
            login (str): адрес электронной почты
            password (str): пароль
        """
        with allure.step(
            "Если появляется капча пытаемся её нажать, иначе продолжаем следующие шаги"
        ):
            try:
                self._driver.find_element(
                    By.CSS_SELECTOR, ".CheckboxCaptcha-Button"
                ).click()
            except NoSuchElementException:
                pass

        with allure.step("Нажимаем кнопку 'Войти' на главной странице сайта"):
            self._driver.find_element(
                By.CSS_SELECTOR, ".styles_loginButton__LWZQp"
            ).click()

        with allure.step("Вводим адрес электронной почты (логин)"):
            self._driver.find_element(By.CSS_SELECTOR, "#passp-field-login").send_keys(
                login
            )

        with allure.step(
            "Нажимаем кнопку 'Войти', на странице ввода логина пользователя"
        ):
            self._driver.find_element(
                By.CSS_SELECTOR, ".passp-button.passp-sign-in-button"
            ).click()

        with allure.step("Вводим пароль"):
            self._driver.find_element(By.CSS_SELECTOR, "#passp-field-passwd").send_keys(
                password
            )

        with allure.step(
            "Нажимаем кнопку 'Войти', на странице ввода пароля пользователя"
        ):
            self._driver.find_element(
                By.CSS_SELECTOR, ".passp-button.passp-sign-in-button"
            ).click()

        with allure.step("Ожидаем возвращения на главную страницу сайта"):
            WebDriverWait(self._driver, 3).until(
                EC.url_contains("https://www.kinopoisk.ru/")
            )
