from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure


class PersonalPage:

    def __init__(self, driver: WebDriver):
        self._driver = driver
        self._driver.get("https://www.kinopoisk.ru")
        self._driver.implicitly_wait(4)
        self._driver.maximize_window()

    def find_element_and_click(self, css_selector: str):
        """
        Данный метод находит элемент на странице по его
        селектору и нажимает на элемент.
        Args:
            css_selector (str): css_selector элемента.
        """
        element = WebDriverWait(self._driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
        )
        element.click()

    def find_element_and_return_text(
        self, element: WebElement, css_selector: str
    ) -> str:
        """
        Данный метод находит элемент на странице по его селектору
        и возращает текст данного элемента.
        Args:
            element: WebElement.
            css_selector (str): css_selector элемента.
        Returns:
            str: текст элемента.
        """
        element = WebDriverWait(element, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector))
        )
        return element.text

    # def find_button_by_text(self, button_text: str) -> WebElement:
    #     """
    #     Метод для поиска кнопки по тексту.
    #     Args:
    #         button_text (str): текст кнопки для поиска.
    #     Returns:
    #         WebElement: найденная кнопка.
    #     """
    #     buttons = WebDriverWait(self._driver, 10).until(
    #         EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[class^='style_buttonContent']"))
    #     )
    #     for button in buttons:
    #         if button.text == button_text:
    #             return button

    def find_button_actions_by_text(self, button_text: str) -> WebElement:
        """
        Метод для поиска кнопки по тексту.
        Args:
            button_text (str): текст кнопки для поиска.
        Returns:
            WebElement: найденная кнопка.
        """
        buttons = WebDriverWait(self._driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "button[class^='style_root']")
            )
        )
        for button in buttons:
            if button.text == button_text:
                return button

    @allure.step("Проверяем устновку оценки.")
    def control_vote(self) -> str:
        """
        Метод считывает установленную фильму или сериалу оценку.
        Returns:
            str: установленная оценка.
        """
        with allure.step(
            "Проверяем какая оценка отображается на странице и возвращаем её значение."
        ):
            div_with_vote = WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div[class^='styles_valueContainer']")
                )
            )
            return self.find_element_and_return_text(
                div_with_vote, "span[class^='styles']"
            )

    @allure.step("Устанавливаем оценку фильму или сериалу. Оценка - {value}.")
    def set_rating(self, value: int):
        """Метод позволяет установить оценку фильму или сериалу.
        Args:
            value (int): укажите значение от 1 до 10.
        """
        with allure.step("На странице нажать кнопку 'Оценить фильм/сериал'"):
            self.find_element_and_click("[class^='styles_kinopoiskRatingSnippet']")

        with allure.step("Установить оценку согласно переданному значению"):
            rating_button_selector = f"button[aria-label='Оценка {value}']"
            self.find_element_and_click(rating_button_selector)

    @allure.step(
        "Изменяем ранее установленную оценку фильму или сериалу. Новая оценка - {new_value}."
    )
    def change_rating(self, new_value: int):
        """Метод позволяет изменить оценку фильму или сериалу.
        Args:
            value (int): укажите новое значение оценки от 1 до 10.
        """
        with allure.step("На странице нажать кнопку 'Изменить оценку'"):
            self.find_element_and_click("[class^='styles_kinopoiskRatingSnippet']")
            self.find_button_actions_by_text("Изменить оценку").click()

        with allure.step("Установить оценку согласно новому переданному значению"):
            rating_button_selector = f"button[aria-label='Оценка {new_value}']"
            self.find_element_and_click(rating_button_selector)

    @allure.step("Удаляем ранее установленную оценку фильму или сериалу.")
    def delete_rating(self):
        """
        Метод позволяет удалить оценку фильму или сериалу.
        """
        with allure.step(
            "На странице фильма или сериала нажать кнопку 'Изменить оценку', затем нажать 'Удалить оценку'"
        ):
            div = self._driver.find_element(
                By.CSS_SELECTOR, "[class^='styles_kinopoiskRatingSnippet']"
            )
            div.click()
            self.find_button_actions_by_text("Удалить оценку").click()
            result = self.find_element_and_return_text(div, "button")
            return result

    @allure.step("Добавляем фильм или сериал в необходимую папку.")
    def add_film_to_folder(self, folder_to_add: str):
        """Метод позволяет добавить фильм или сериали в необходимую папку.
        Args:
            folder_to_add (str): название папки, в которую необходимо добавить фильм.
        """
        with allure.step(
            "На странице фильма, нажимаем на кнопку 'Добавить в папку', затем добавляем в необходимую папку."
        ):
            self.find_element_and_click("button[title='Добавить в папку']")
            folder_buttons = self._driver.find_elements(
                By.CSS_SELECTOR, "span[class^='styles_name']"
            )
            for button in folder_buttons:
                if button.text == folder_to_add:
                    button.click()
