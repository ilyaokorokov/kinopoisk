from typing import Tuple
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure


class UserProfile:

    def __init__(self, driver: WebDriver):
        self._driver = driver
        self._driver.get("https://www.kinopoisk.ru")
        self._driver.implicitly_wait(4)
        self._driver.maximize_window()

    @allure.step("Разворачиваем меню пользователя.")
    def open_profile(self):
        """Метод позволяет развернуть меню пользователя."""
        self._driver.find_element(
            By.CSS_SELECTOR, "button[aria-label='Меню профиля']"
        ).click()

    @allure.step("Переходим в кабинет пользователя.")
    def enter_profile(self):
        """Метод позволяет перейти в полноценный кабинет пользователя."""
        self.open_profile()
        self._driver.find_element(By.CSS_SELECTOR, "a[href^='/user/']").click()

    @allure.step(
        "Открываем в кабинете пользователя необходимый раздел согласно переданному названию."
    )
    def user_profile_section_buttons(self, name_section: str):
        """Метод открывает раздел в личном кабинете
        согласно переданному названию раздела.
        Args:
            name_section: название раздела (Профиль, Рецензии, Оценки, Комментарии, Друзья, Фильмы, Звёзды, Списки).
        """
        buttons = self._driver.find_elements(By.CSS_SELECTOR, "li[class^='menuButton']")
        for button in buttons:
            all_a = button.find_elements(By.CSS_SELECTOR, "a")
            for element in all_a:
                if element.text == name_section:
                    element.click()
                    return

    @allure.step("В разделе Фильмы собираем информацию и возвращаем её.")
    def film_personal_profile_section(self) -> Tuple[str, list, list]:
        """Метод собирает информацию со страницы фильмов
        в кабинете пользователя и возвращает её.
        Returns:
            str: счетчик количества фильмов в папке "Буду смотреть"
            list: количество фильмов в папке
            list: список с названиями фильмов
        """
        with allure.step(
            "Собираем информацию о счётчике количества фильмов в папке 'Буду смотреть'"
        ):
            folder_to_watch = WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.isWatchFolders"))
            )
            counter_films_folder = WebDriverWait(folder_to_watch, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "i.num"))
            )
            counter_text = counter_films_folder.text
            number_counter = counter_text.strip("()")
        with allure.step("Собираем информацию о количестве фильмов и названии фильмов"):
            list_films = WebDriverWait(self._driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li[id^='film']"))
            )
            films_title = []
            for film in list_films:
                a_element = film.find_element(By.CSS_SELECTOR, "a.name")
                films_title.append(a_element.text)
        with allure.step(
            "Возвращаем информацию о счётчике количестве книг, фактическом количестве книг, списке с названиями фильмов."
        ):
            return number_counter, list_films, films_title

    @allure.step("В разделе Оценки об оценке фильма, название которого передали.")
    def get_film_vote_personal_section(self, film_name: str) -> str:
        """Данный метод позволяет получить оценку фильма в кабинете
        пользователя согласно переданному названию фильма.
        Returns:
            str: возвращает оценку фильма
        """
        with allure.step("Ожидание загрузки списка фильмов и оценок"):
            div_films = WebDriverWait(self._driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.item"))
            )

        with allure.step("Поиск нужного фильма и получение его оценки"):
            for div in div_films:
                film_title_element = WebDriverWait(div, 10).until(
                    EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, "a[href^='/film/']")
                    )
                )
                if film_name in film_title_element.text:
                    vote_element = WebDriverWait(div, 10).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.vote"))
                    )
                    return vote_element.text
                    break
