import allure


@allure.feature("Поиск фильма/сериала.")
@allure.title("Тест на получение информации о фильме/сериале по названию.")
@allure.description("Получаем информацию согласно переданному названию.")
@allure.id(1)
@allure.severity("Blocker")
def test_get_film_tv_series_by_name(api):
    film_tv_series = "Аватар"
    result_search_by_name, status_code = api.search_film_tv_series_by_name(
        film_tv_series
    )
    assert status_code == 200
    assert result_search_by_name["docs"][1]["name"] == "Аватар"


@allure.feature("Поиск фильма/сериала.")
@allure.title("Тест на получение информации о фильме/сериале по его id номеру.")
@allure.description(
    "Получаем информацию согласно переданному id номеру фильма или сериала."
)
@allure.id(2)
@allure.severity("Blocker")
def test_get_film_tv_series_by_id(api, film_id):
    result_search_by_id, status_code = api.search_film_tv_series_by_id(film_id)
    assert status_code == 200
    assert result_search_by_id["name"] == "Аватар"


@allure.feature("Поиск фильма/сериала.")
@allure.title("Тест на получение информации о фильме/сериале по переданным полям.")
@allure.description("Получаем информацию согласно переданным полям.")
@allure.id(3)
@allure.severity("Critical")
def test_get_film_tv_series_by_field(api):
    film_tv_series_field = "genres.name"
    result_search_by_field, status_code = api.search_by_fields(film_tv_series_field)
    assert status_code == 200
    assert "детектив" in [genre["name"] for genre in result_search_by_field]


@allure.feature("Поиск персоны.")
@allure.title("Тест на получение информации о персоне по имени и фамилии.")
@allure.description("Получаем информацию согласно переданному имени и фамилии.")
@allure.id(4)
@allure.severity("Blocker")
def test_search_person_by_name(person_api):
    person_name = "Леонардо ДиКаприо"
    result_search_person_by_name, status_code = person_api.search_person_by_name(
        person_name
    )
    assert status_code == 200
    assert result_search_person_by_name["docs"][0]["name"] == person_name


@allure.feature("Поиск персоны.")
@allure.title("Тест на получение информации о персоне по id номеру.")
@allure.description("Получаем информацию согласно переданному id номеру персоны.")
@allure.id(5)
@allure.severity("Blocker")
def test_search_person_by_id(person_id, person_api):
    person_name = "Леонардо ДиКаприо"
    result_search_person_by_name, status_code = person_api.search_person_by_name(
        person_name
    )
    assert status_code == 200
    assert result_search_person_by_name["docs"][0]["name"] == person_name
