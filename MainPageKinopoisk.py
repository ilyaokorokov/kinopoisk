from typing import Tuple, List
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import allure


class Main:

    def __init__(self, driver: WebDriver):
        self._driver = driver
        self._driver.get("https://www.kinopoisk.ru")
        self._driver.implicitly_wait(4)
        self._driver.maximize_window()

    @allure.step("Обрабатываем капчу, если она появляется.")
    def captcha(self):
        """
        Данный метод обрабатывает капчу.
        """
        try:
            self._driver.find_element(
                By.CSS_SELECTOR, ".CheckboxCaptcha-Button"
            ).click()
        except NoSuchElementException:
            pass

    @allure.step("Вводим данные в поле поиска: {info_to_search}")
    def enter_search_info(self, info_to_search: str):
        """
        Данный метод вводит данные в поисковое поле.
        Args:
            info_to_search (str): информация для поиска.
        """
        search_field = self._driver.find_element(
            By.CSS_SELECTOR,
            ".kinopoisk-header-search-form-input__input[aria-label='Фильмы, сериалы, персоны']",
        )
        search_field.click()
        search_field.send_keys(info_to_search)

    @allure.step("Получаем текст элементов в подсказках к поисковому полю.")
    def get_search_field_list(self, selector: str) -> List[str]:
        """Данный метод собирает список элементов
        в подсказках к модулю поиска.
        Args:
            selector (str): селектор веб элемента.
        Returns:
            list: возвращает список элементов.
        """
        elements = self._driver.find_elements(By.CSS_SELECTOR, selector)
        return [element.text for element in elements]

    @allure.step("Нажимаем кнопку поиска")
    def click_search_button(self):
        """
        Данный метож нажимает на кнопку поиска в модуле поиска.
        """
        self._driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    @allure.step("Ожидаем и возвращаем элемент на странице результата поиска.")
    def get_element_from_search_result_page(
        self, css_selector: str
    ) -> Tuple[WebElement, str]:
        """Данный метод ожидает появление элемента на странице.
        Возвращает данный веб элемент и текст ссылки.
        Args:
            css_selector (str): селектор элемента.
        Returns:
            Tuple[WebElement, str]: веб элемент и текст ссылки.
        """
        element = WebDriverWait(self._driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
        )
        div_info = element.find_element(By.CSS_SELECTOR, "div.info")
        p_name_result_search_page = div_info.find_element(By.CSS_SELECTOR, "p.name")
        a_link = p_name_result_search_page.find_element(By.CSS_SELECTOR, "a")
        text_link = a_link.text
        return a_link, text_link

    @allure.step(
        "Переходим на сайт Кинопоиск. Выполняем поиск фильма или сериала. Название - {info_to_search}."
    )
    def search_film_or_tv_series(self, info_to_search: str) -> str:
        """Метод позволяет выполнить поиск фильма или сериала
        используя информацию полученную на вход.
        Открыть персональную карточку фильма или сериала.
        Args:
            info_to_search (str): название фильма или сериала.
        Returns:
            str: возвращает название фильма или сериала из подсказки к поисковому полю, страницы результата поиска, персональной страницы фильма или сериала.
        """
        self.captcha()
        self.enter_search_info(info_to_search)
        found_movie_titles = self.get_search_field_list("[id^='suggest-item']")
        self.click_search_button()
        a_film_link, film_text_link = self.get_element_from_search_result_page(
            "div.element.most_wanted"
        )
        a_film_link.click()

        with allure.step("На странице фильма или сериала получаем его название."):
            name_film_personal_page = WebDriverWait(self._driver, 10).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "h1[itemprop='name']")
                )
            )

        with allure.step(
            "Возвращаем список с 1 фильмом или сериалом из подсказки к поисковому полю, название фильма или сериала на странице результата поиска, название с персональной страницы."
        ):
            return (
                found_movie_titles,
                film_text_link,
                name_film_personal_page.text,
            )

    @allure.step(
        "Переходим на сайт Кинопоиск. Выполняем поиск персоны. Фамилия и имя персоны - {info_to_search}."
    )
    def search_person(self, info_to_search: str) -> str:
        """Метод позволяет выполнить поиск персоны
        используя информацию полученную на вход.
        Отрыть личную карточку персоны.

        Args:
            info_to_search (str): фамилия и имя персоны.
        Returns:
            str: возвращает список с 1 персоной из подсказки к поисковому полю, фамилию и имя персоны на странице результата поиска, фамилию и имя с личной страницы персоны.
        """
        self.captcha()
        self.enter_search_info(info_to_search)
        found_person_titles = self.get_search_field_list("[id^='suggest-item-person']")
        self.click_search_button()
        a_person_link, person_text_link = self.get_element_from_search_result_page(
            "div.element.most_wanted"
        )
        a_person_link.click()

        with allure.step("На странице персоны получаем фамилию и имя."):
            name_surname_person_private_page = WebDriverWait(self._driver, 10).until(
                EC.visibility_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "[class^='styles_primaryName']",
                    )
                )
            )

        with allure.step(
            "Возвращаем список с 1 персоной из подсказки к поисковому полю, фамилию и имя персоны на странице результата поиска, фамилию и имя с личной страницы персоны."
        ):
            return (
                found_person_titles,
                person_text_link,
                name_surname_person_private_page.text,
            )

    @allure.step(
        "Переходим на сайт Кинопоиск. Выполняем поиск по несуществующему названию. Проверяем информационное сообщение."
    )
    def empty_search(self, info_to_search: str) -> str:
        """Метод позволяет выполнить поиск по несуществующему названию
        и проверить корректность выдачи информационного сообщения.
        Args:
            info_to_search (str): введите несуществующее название.
        Returns:
            str: текст информационного сообщения.
        """
        self.captcha()
        self.enter_search_info(info_to_search)
        self.click_search_button()

        with allure.step("Считываем текст информационного сообщения и возвращаем его."):
            message_empty_result = self._driver.find_element(
                By.CSS_SELECTOR, "h2.textorangebig"
            ).text
            return message_empty_result
