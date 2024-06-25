import requests

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
auth_page = Auth(driver)
main_page = Main(driver)
personal_page = PersonalPage(driver)
