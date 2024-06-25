import requests
from Auth import Auth


class FilmTvSeriesApi:
    def __init__(self, url):
        self.url = url
        self.auth = Auth(url)

    def get_employee_list(self, company_id):
        employee_list = requests.get(
            self.url + "/employee" + "?company=" + str(company_id)
        )
        return employee_list.json(), employee_list.status_code

    def get_employee_by_id(self, id):
        result_get_employee_id = requests.get(self.url + "/employee/" + str(id))
        return result_get_employee_id.json(), result_get_employee_id.status_code
