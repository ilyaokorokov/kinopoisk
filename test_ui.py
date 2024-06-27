from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from AuthPageKinopoisk import Auth
from MainPageKinopoisk import Main
from FilmSeriesPageKinopoisk import PersonalPage
from UserPageKinopoisk import UserProfile
import allure
import pytest
import json

with open("config.json", "r") as config_file:
    config = json.load(config_file)

base_url_ui = config.get("base_url_ui")
auth_credentials = config.get("auth_credentials")


@pytest.fixture()
def browser():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    yield driver
    driver.quit()


@pytest.fixture
def auth_page(browser):
    return Auth(browser)


@pytest.fixture
def main_page(browser):
    return Main(browser)


@pytest.fixture
def personal_page(browser):
    return PersonalPage(browser)


@pytest.fixture
def user_profile_page(browser):
    return UserProfile(browser)


@allure.feature("Авторизация на сайте.")
@allure.title("Тест авторизации пользователя.")
@allure.description("Авторизуемся на сайте используя входные данные.")
@allure.id(1)
@allure.severity("Blocker")
def test_auth(auth_page):
    auth_page.user_auth(auth_credentials["username"], auth_credentials["password"])
    with allure.step(
        "Проверяем вернулись ли мы на главную страницу после авторизации."
    ):
        expected_url = base_url_ui
        actual_url = auth_page._driver.current_url
        assert actual_url.startswith(expected_url)


@allure.feature("Модуль поиска.")
@allure.title("Тест на поиск фильма или сериала.")
@allure.description("Выполняем поиск фильма или сериала согласно полученным данным.")
@allure.id(2)
@allure.severity("Blocker")
def test_search_film_tv_series(main_page):
    film_tv_series = "Гарри Поттер"
    film_name_search_list, film_name_result_search, film_name_personal_page = (
        main_page.search_film_or_tv_series(film_tv_series)
    )
    with allure.step(
        "Проверяем, что переданное название фильма совпадает с названием выводимым в подсказках к модулю поиска, на странице результата поиска, на персональной странице фильма."
    ):
        assert film_tv_series in film_name_search_list[0]
        assert film_name_result_search.startswith(film_tv_series)
        assert film_name_personal_page.startswith(film_tv_series)


@allure.feature("Модуль поиска.")
@allure.title("Тест на поиск персоны.")
@allure.description("Выполняем поиск персоны согласно полученным данным.")
@allure.id(3)
@allure.severity("Blocker")
def test_search_person(main_page):
    person_info = "Александр Петров"
    person_info_search_list, person_info_result_search, person_info_private_page = (
        main_page.search_person(person_info)
    )
    with allure.step(
        "Проверяем, что переданные фамилия и имя персоны совпадают с данными выводимыми в подсказках к модулю поиска, на странице результата поиска, на личной странице персоны."
    ):
        assert person_info in person_info_search_list[0]
        assert person_info_result_search == person_info
        assert person_info_private_page == person_info


@allure.feature("Модуль поиска.")
@allure.title("Тест поиск по несуществующему названию.")
@allure.description(
    "Выполняем поиск по несуществующему названию, проверяем корректность выдачи информационного сообщения."
)
@allure.id(4)
@allure.severity("Normal")
def test_empty_search_info_message(main_page):
    search_info = "no book such term"
    message = "К сожалению, по вашему запросу ничего не найдено..."
    get_message = main_page.empty_search(search_info)
    with allure.step(
        "Проверяем, что считанное информационное сообщение идентично шаблону."
    ):
        assert get_message == message


@allure.feature("Установка оценки.")
@allure.title("Тест на установку оценки фильму или сериалу.")
@allure.description(
    "Авторизуемся, выполняем поиск фильма или сериала, устанавливаем оценку."
)
@allure.id(5)
@allure.severity("Blocker")
def test_set_rating_for_film_or_tv_series(auth_page, main_page, personal_page):
    auth_page.user_auth(auth_credentials["username"], auth_credentials["password"])
    film_tv_series = "Артур, ты король"
    film_name_search_list, film_name_result_search, film_name_personal_page = (
        main_page.search_film_or_tv_series(film_tv_series)
    )
    first_value = 3
    second_value = 10
    button_text = "Оценить фильм"
    personal_page.set_rating(first_value)
    control_first = personal_page.control_vote()
    assert str(first_value) == control_first
    personal_page.change_rating(second_value)
    control_second = personal_page.control_vote()
    assert str(second_value) == control_second
    deleted_rating_button_text = personal_page.delete_rating()
    assert deleted_rating_button_text == button_text


@allure.feature("Установка оценки.")
@allure.title(
    "Тест на установку оценки фильму или сериалу и проверку оценки в профиле пользователя."
)
@allure.description(
    "Авторизуемся, выполняем поиск фильма или сериала, устанавливаем оценку, выпоняем проверку оценки в профиле пользователя."
)
@allure.id(6)
@allure.severity("Critical")
def test_set_rating_for_film_or_tv_series_and_check(
    auth_page, main_page, personal_page, user_profile_page
):
    auth_page.user_auth(auth_credentials["username"], auth_credentials["password"])
    film_tv_series = "Аватар"
    film_name_search_list, film_name_result_search, film_name_personal_page = (
        main_page.search_film_or_tv_series(film_tv_series)
    )
    with allure.step("Устанавливаем и проверяем, оценку на странице фильма/сериала."):
        first_value = 10
        personal_page.set_rating(first_value)
        control_first = personal_page.control_vote()
        assert str(first_value) == control_first
    with allure.step(
        "Переходим в профиль пользователя и проверяем, оценку на в разделе Оценки."
    ):
        user_profile_page.enter_profile()
        user_profile_page.user_profile_section_buttons("Оценки")
        user_profile_film_vote = user_profile_page.get_film_vote_personal_section(
            film_tv_series
        )
        assert str(first_value) == user_profile_film_vote
        i, k, m = main_page.search_film_or_tv_series(film_tv_series)
        deleted_rating_button_text = personal_page.delete_rating()
        assert deleted_rating_button_text == "Оценить фильм"


@allure.feature("Добавление фильма/сериала в папку.")
@allure.title("Тест на добавление фильма или сериала в необходимую папку.")
@allure.description(
    "Авторизуемся, выполняем поиск фильма или сериала, добавляем его в необходимую папку, выполняем проверки."
)
@allure.id(7)
@allure.severity("Critical")
def test_add_film_or_tv_series_to_folder(
    auth_page, main_page, personal_page, user_profile_page
):
    auth_page.user_auth(auth_credentials["username"], auth_credentials["password"])
    film_tv_series = "Аватар"
    film_name_search_list, film_name_result_search, film_name_personal_page = (
        main_page.search_film_or_tv_series(film_tv_series)
    )
    personal_page.add_film_or_person_to_folder("Буду смотреть")
    user_profile_page.enter_profile()
    user_profile_page.user_profile_section_buttons("Фильмы")
    counter, films, titles = user_profile_page.film_personal_profile_section()
    assert counter == "3"
    assert len(films) == int(counter)
    assert titles[0] == film_tv_series
    i, k, m = main_page.search_film_or_tv_series(film_tv_series)
    personal_page.add_film_or_person_to_folder("Буду смотреть")
