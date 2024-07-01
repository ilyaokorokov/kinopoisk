from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from AuthPageKinopoisk import Auth
from MainPageKinopoisk import Main
from FilmSeriesPageKinopoisk import PersonalPage
from UserPageKinopoisk import UserProfile
from FilmTvSeriesApi import FilmTvSeriesApi
from PersonApi import PersonApi
import pytest
import json


with open("config.json", "r") as config_file:
    config = json.load(config_file)

base_url_api = config.get("base_url_api")
token_info = config.get("token_info")


@pytest.fixture
def browser():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get("https://www.kinopoisk.ru")
    driver.implicitly_wait(4)
    driver.maximize_window()
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


@pytest.fixture
def api():
    return FilmTvSeriesApi(base_url_api)


@pytest.fixture
def person_api():
    return PersonApi(base_url_api)


@pytest.fixture()
def film_id(api):
    film_tv_series = "Аватар"
    result_search_by_name, status_code = api.search_film_tv_series_by_name(
        film_tv_series
    )
    assert status_code == 200
    assert result_search_by_name["docs"][0]["name"] == "Аватар"
    print(result_search_by_name["docs"][0]["id"])
    return result_search_by_name["docs"][0]["id"]


@pytest.fixture()
def person_id(person_api):
    person_name = "Леонардо ДиКаприо"
    result_search_person_by_name, status_code = person_api.search_person_by_name(
        person_name
    )
    assert status_code == 200
    print(result_search_person_by_name["docs"][0]["id"])
    return result_search_person_by_name["docs"][0]["id"]
