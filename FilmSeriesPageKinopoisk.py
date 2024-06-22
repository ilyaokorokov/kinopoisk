from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure


class PersonalPage:

    def __init__(self, driver: str):
        self._driver = driver
        self._driver.get("https://www.kinopoisk.ru")
        self._driver.implicitly_wait(10)
        self._driver.maximize_window()

    def find_element_and_click(self, xpath: str):
        """
        Данный метод находит элемент на странице по его
        XPATH и нажимает на элемент.

        Args:
            xpath (str): полный путь к элементу
        """
        element = WebDriverWait(self._driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        element.click()

    def find_element_and_return_text(self, xpath: str) -> str:
        """
        Данный метод находит элемент на странице по его XPATH
        и возращает текст данного элемента.

        Args:
            xpath (str): полный путь к элементу

        Returns:
            str: текст элемента
        """
        element = WebDriverWait(self._driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, xpath))
        )
        return element.text

    @allure.step("Устанавливаем оценку фильму или сериалу. Оценка - {value}.")
    def set_rating(self, value: int) -> str:
        """Метод позволяет установить оценку фильму или сериалу.

        Args:
            value (int): укажите значение от 1 до 10

        Returns:
            str: возвращает значение установленной оценки
        """

        with allure.step("На странице нажать кнопку 'Оценить фильм/сериал'"):
            self.find_element_and_click(
                "/html/body/div[1]/div[1]/div[2]/div[2]/div[2]/div/div[3]/div/div/div[1]/div[2]/div/div[2]/div/button"
            )

        with allure.step("Установить оценку согласно переданному значению"):
            div_rating = WebDriverWait(self._driver, 10).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "/html/body/div[1]/div[1]/div[2]/div[2]/div[2]/div/div[3]/div/div/div[1]/div[2]/div/div[2]/div/div/div",
                    )
                )
            )
            rating_buttons_text = div_rating.find_elements(By.CSS_SELECTOR, "span")
            for element in rating_buttons_text:
                if str(value) in element.text:
                    element.click()

        with allure.step("Считывает установленную оценку и возвращаем это значение"):
            self._driver.refresh()
            rating = self.find_element_and_return_text(
                "/html/body/div[1]/div[1]/div[2]/div[3]/div/div/div[1]/div/div[2]/div/div/div[3]/div/div/div[1]/div[1]/div/div[1]/span"
            )
            return rating

    @allure.step(
        "Изменяем ранее установленную оценку фильму или сериалу. Новая оценка - {new_value}."
    )
    def change_rating(self, new_value: int) -> str:
        """Метод позволяет изменить оценку фильму или сериалу.

        Args:
            value (int): укажите новое значение оценки от 1 до 10

        Returns:
            str: возвращает значение новой установленной оценки
        """

        with allure.step("На странице нажать кнопку 'Изменить оценку'"):
            self._find_element_and_click(
                "/html/body/div[1]/div[1]/div[2]/div[2]/div[2]/div/div[3]/div/div/div[1]/div[2]/div/div[2]/div/div/div/button"
            )
            self._find_element_and_click(
                "/html/body/div[1]/div[1]/div[2]/div[2]/div[2]/div/div[3]/div/div/div[1]/div[2]/div/div[2]/div/div/div[2]/div/button[1]"
            )

        with allure.step("Установить оценку согласно новому переданному значению"):
            div_rating = self._driver.find_element(
                By.XPATH,
                "/html/body/div[1]/div[1]/div[2]/div[2]/div[2]/div/div[3]/div/div/div[1]/div[2]/div/div[2]/div/div/div",
            )
            rating_buttons_text = div_rating.find_elements(By.CSS_SELECTOR, "span")
            for element in rating_buttons_text:
                if str(new_value) in element.text:
                    element.click()

        with allure.step("Считывает установленную оценку и возвращаем это значение"):
            new_rating = self._find_element_and_return_text(
                "/html/body/div[1]/div[1]/div[2]/div[2]/div[2]/div/div[3]/div/div/div[1]/div[2]/div/div[2]/div/div/div/button/div/span[2]/span[2]"
            )
            return new_rating

    @allure.step("Удаляем ранее установленную оценку фильму или сериалу.")
    def delete_rating(self) -> str:
        """
        Метод позволяет удалить оценку фильму или сериалу.

        Returns:
            str: текст кнопки без установленной оценки
        """

        with allure.step(
            "На странице фильма или сериала нажать кнопку 'Изменить оценку', затем нажать 'Удалить оценку'"
        ):
            self._find_element_and_click(
                "/html/body/div[1]/div[1]/div[2]/div[2]/div[2]/div/div[3]/div/div/div[1]/div[2]/div/div[2]/div/div/div/button"
            )
            self._find_element_and_click(
                "/html/body/div[1]/div[1]/div[2]/div[2]/div[2]/div/div[3]/div/div/div[1]/div[2]/div/div[2]/div/div/div[2]/div/button[2]"
            )
            set_rating_button = self._driver.find_element(
                By.XPATH,
                "/html/body/div[1]/div[1]/div[2]/div[2]/div[2]/div/div[3]/div/div/div[1]/div[2]/div/div[2]/div/button",
            )
            return set_rating_button.text
