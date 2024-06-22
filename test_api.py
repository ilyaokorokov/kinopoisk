from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from AuthPageKinopoisk import Auth
from MainPageKinopoisk import Main
from FilmSeriesPageKinopoisk import PersonalPage
import allure

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
auth_page = Auth(driver)
main_page = Main(driver)
personal_page = PersonalPage(driver)
