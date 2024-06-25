from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class UserProfileMainPage:
    
    def __init__(self, driver):
        self._driver = driver
        self._driver.get("https://www.kinopoisk.ru/")
        self._driver.implicitly_wait(4)
        self._driver.maximize_window()

    # def open_profile(self): 
    #     """Метод позволяет развернуть меню пользователя.
    #     """
    #     self._driver.find_element(By.CSS_SELECTOR, "button[aria-label='Меню профиля']").click()

    # def enter_profile(self):
    #     """Метод позволяет перейти в полноценный кабинет пользователя.
    #     """
    #     self.open_profile(self)
    #     self._driver.find_element(By.CSS_SELECTOR, "a[href^='/user/']").click()

    def profile_buttons(self, text_value: str):
        """Метод собирает информацию по доступным кнопкам в меню пользователя
        и нажимает на необходимую кнопку в зависимости от переданного текста
        этой кнопки.
        """
        div = self._driver.find_element(By.CSS_SELECTOR, "ul[class^='styles_navigationGroup']")
        all_a = div.find_elements(By.CSS_SELECTOR, "a[class^='styles_menuLink']")
        for a in all_a:
            if a.text == text_value:
                a.click()

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








    def user_profile_section_buttons(self, name_section: str):
        """Метод открывает раздел в личном кабинете, согласно переданному названию раздела.
        Args:
            name_section: название раздела (Профиль, Рецензии, Оценки, Комментарии, Друзья, Фильмы, Звёзды, Списки).
        """
        buttons = self._driver.find_elements(By.CSS_SELECTOR, "li[class^='menuButton']")
        all_a = buttons.find_elements(By.CSS_SELECTOR, "a")
        for element in all_a:
            if element.text == name_section:
                element.click()
                break
    
    def film_personal_profile_section(self) -> Tuple[str, list, list]:
        """Метод собирает информацию со страницы фильмов в кабинете пользователя и возвращает её.
        Returns:
            str: счетчик количества фильмов в папке "Буду смотреть"
            list: количество фильмов в папке
            list: список с названиями фильмов
        """
        folder_to_watch = self._driver.find_element(By.CSS_SELECTOR, "div.isWatchFolders")
        counter_films_folder = folder_to_watch.find_element(By.CSS_SELECTOR, "i.num")
        counter_text = counter_films_folder.text
        number_counter = counter_text.strip('()')
        list_films = self._driver.find_elements(By.CSS_SELECTOR, "li[id^='film']")
        films_title = []
        for film in list_films:
            a_element = film.find_element(By.CSS_SELECTOR, "a")
            films_title.append(a_element.text)
        return number_counter, list_films, films_title
        
        assert str(len(list_films)) == number_counter








    def get_film_vote(self, film_name: str)-> str:
        """Данный метод позволяет получить оценку фильма
        согласно переданному названию фильма. (В ПРОФИЛЕ - ОЦЕНКИ В ПРОФИЛЕ ОЦЕНКИ)
        Returns:
            str: возвращает оценку фильма
        """
        div_films = self._driver.find_elements(By.CSS_SELECTOR, "div.item")
        div_num_film = self._driver.find_elements(By.CSS_SELECTOR, "div.num")
        a_films = self._driver.find_elements(By.CSS_SELECTOR, "a[href^='/film/']")
        vote_films = self._driver.find_elements(By.CSS_SELECTOR, "div.vote")
        for i in range(len(a_films)):
            if film_name in a_films[i].text:
                return vote_films[i].text


ПЕРСОНА ДУБЛИКАТ В ФИЛЬМЕ
    def add_to_folder(self, folder_to_add: str):
        """Метод добавляет фильм в папку название которой мы передали.
        """
        folder_buttons = self._driver.find_elements(By.CSS_SELECTOR, "span[class^='styles_name']")
        for button in folder_buttons:
            if button.text == folder_to_add:
                button.click()
                break




class FilmPage:

    # def open_folders(self):
    #     """Метод открывает список папок (МОЖНО ФАЙНД ЭЛЕМЕНТ И КЛИК).
    #     """
    #     add_button = self._driver.find_element(By.CSS_SELECTOR, "button[title='Добавить в папку']")
    #     add_button.click()    

    # def add_film_or_person_to_folder(self, folder_to_add: str):
    #     """Метод добавляет фильм в папку название которой мы передали.
    #     """
    #     self._driver.find_element(By.CSS_SELECTOR, "button[title='Добавить в папку']").click()
    #     folder_buttons = self._driver.find_elements(By.CSS_SELECTOR, "span[class^='styles_name']")
    #     for button in folder_buttons:
    #         if button.text == folder_to_add:
    #             button.click()
    #             break


    def add_to_will_watch(self):
        """
        Добавляет фильм в папку Буду смотреть
        """
        self.find_element_and_click("button[title='Буду смотреть']")









    def set_vote(self, vote: int)->str:
        """Метод устанавливает оценку фильму, согласно переданному значению.
        """
        votes_button = self._driver.find_elements(By.CSS_SELECTOR, "span[class^='styles_text']")
        for element in votes_button:
            if element.text == str(vote):
                element.click()      
                break
        div_with_vote = WebDriverWait(self._driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[class^='styles_valueContainer']"))
        )
        span = div_with_vote.find_element(By.CSS_SELECTOR, "span")
        return span.text