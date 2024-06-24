from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class UserProfileMainPage:
    
    def __init__(self, driver):
        self._driver = driver
        self._driver.get("https://www.kinopoisk.ru/")
        self._driver.implicitly_wait(4)
        self._driver.maximize_window()

    def open_profile(self): 
        """Метод позволяет развернуть меню пользователя.
        """
        self._driver.find_element(By.CSS_SELECTOR, "button[aria-label='Меню профиля']").click()

    def enter_profile(self):
        """Метод позволяет перейти в полноценный кабинет пользователя.
        """
        self.open_profile(self)
        self._driver.find_element(By.CSS_SELECTOR, "a[href^='/user/']").click()

    def add_family_button(self)->str:
        """Метод позволяет перейти на страницу добавления пользователя в семью.
        Returns:
            str: URL страницы добавления пользователя в семью.
        """
        self.open_profile()
        self._driver.find_element(By.CSS_SELECTOR, "a[href^='https://passport.yandex.ru/family']").click()
        WebDriverWait(self._driver, 10).until(EC.url_to_be("https://id.yandex.ru/family?dialog=create-invite&utm_source=kinopoisk"))
        actual_url = self._driver.current_url
        return actual_url

    def add_account_button(self)->str:
        """Метод позволяет перейти на страницу добавления нового аккаунта.
        Returns:
            str: URL страницы авторизации/добавления аккаунта.
        """
        self.open_profile()
        div = self._driver.find_element(By.CSS_SELECTOR, "div[class^='styles_multiAuth']")
        button_account = div.find_element(By.CSS_SELECTOR, "button[class^='styles_menuButton']")
        button_account.click()
        WebDriverWait(self._driver, 10).until(EC.url_contains("https://passport.yandex.ru/auth"))
        actual_url = self._driver.current_url
        return actual_url

    def profile_buttons(self, text_value: str):
        """Метод собирает информацию по доступным кнопкам в меню пользователя
        и нажимает на необходимую кнопку в зависимости от переданного текста
        этой кнопки.
        """
        #контейнер с позициями оценки фильмы и тд
        div = self._driver.find_element(By.CSS_SELECTOR, "ul[class^='styles_navigationGroup']")
        all_a = div.find_elements(By.CSS_SELECTOR, "a[class^='styles_menuLink']")
        for a in all_a:
            if a.text == text_value:
                a.click()

    def get_film_vote(self, film_name: str)-> str:
        """Данный метод позволяет получить оценку фильма
        согласно переданному названию фильма.
        Returns:
            str: возвращает оценку фильма
        """
        div_films = self._driver.find_elements(By.CSS_SELECTOR, "div.item")
        len(div_films) количество фильмов
        div_num_film = self._driver.find_elements(By.CSS_SELECTOR, "div.item")
        a_films = self._driver.find_elements(By.CSS_SELECTOR, "a[href^='/film/']")
        vote_films = self._driver.find_elements(By.CSS_SELECTOR, "div.vote")
        for i in range(len(a_films)):
            if film_name in a_films[i].text:
                return vote_films[i].text






class FilmPage:

    # def open_folders(self):
    #     """Метод открывает список папок (МОЖНО ФАЙНД ЭЛЕМЕНТ И КЛИК).
    #     """
    #     add_button = self._driver.find_elements(By.CSS_SELECTOR, "button[title='Добавить в папку']")
    #     add_button.click()    

    # def add_film_to_folder(self, folder_to_add: str):
    #     """Метод добавляет фильм в папку название которой мы передали.
    #     """
    #     folder_buttons = self._driver.find_elements(By.CSS_SELECTOR, "span[class^='styles_name']")
    #     for button in folder_buttons:
    #         if button.text == folder_to_add:
    #             button.click()

    # def set_vote(self, vote: int)->str:
    #     """Метод устанавливает оценку фильму, согласно переданному значению.
    #     """
    #     votes_button = self._driver.find_elements(By.CSS_SELECTOR, "span[class^='styles_text']")
    #     for element in votes_button:
    #         if element.text == str(vote):
    #             element.click()
        
    #     div_with_vote = WebDriverWait(self._driver, 10).until(
    #         EC.presence_of_element_located((By.CSS_SELECTOR, "div[class^='styles_valueContainer']"))
    #     )
    #     span = div_with_vote.find_element(By.CSS_SELECTOR, "span")
        
    #     return span.text