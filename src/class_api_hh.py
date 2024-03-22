import requests
import json


class HeadhunterVacancy:
    """Получение вакансий с платформы HeadHunter API"""
    HH_URL = "https://api.hh.ru/vacancies"
    HH_COMPANY = "https://api.hh.ru/employers"
    HH_AREAS = "https://api.hh.ru/suggests/areas"
    company_id = 'company_id_hh.json'

    def __init__(self, city_name):
        self.city_name = city_name

    def __repr__(self):
        return f"Указанный город: {self.city_name}"

    @property
    def get_city_id(self):
        """Получение id города для получения в нем вакансий"""
        params = {
            "text": self.city_name
        }
        hh_areas_url = self.HH_AREAS
        response = requests.get(hh_areas_url, params=params)

        for city in response.json()["items"]:
            if city["text"] == self.city_name:
                return city["id"]

    @property
    def company_name(self):
        """
		Функция получения id работодателя на платформе headhunter из файла
		:return: list
		"""
        company_list = []
        with open(self.company_id, 'r', encoding='utf-8') as file:
            company_json = json.load(file)
            for item in company_json:
                company_list.append(item['name'])
        return company_list

    @property
    def get_company_id(self):
        """
		Функция получения id работодателя на платформе headhunter из файла
		:return: list
		"""
        company_id_list = []
        with open(self.company_id, 'r', encoding='utf-8') as file:
            company_json = json.load(file)
            for item in company_json:
                company_id_list.append(item['id'])
        return company_id_list

    @property
    def get_json_name(self):
        """
		Функция получения id работодателя на платформе headhunter из файла
		:return: list
		"""
        company_name_list = []
        with open(self.company_id, 'r', encoding='utf-8') as file:
            company_json = json.load(file)
            for item in company_json:
                company_name_list.append(item['name'])
        return company_name_list

    def company_information(self):
        """
		Функция получения всех данных о работодателях
		:return: list
		"""
        company_info = []
        company_info_shorten = []
        for item in self.get_company_id:
            hh_areas_url = f'https://api.hh.ru/employers/{item}'
            response = requests.get(hh_areas_url)
            info_company = response.json()
            company_info.append(info_company)
        for company in company_info:
            shorten_items = {
                "company_id": int(company['id']),
                "name": company['name'],
                "url_company": company['site_url'],
                "url_company_hh": company['alternate_url'],
                "city": company['area']['name'],
            }
            company_info_shorten.append(shorten_items)
        return company_info_shorten

    def get_vacancies(self):
        """Получение всех вакансий работодателей"""
        vacancies_list = []
        vacancies_shorten = []
        hh_vac_url = self.HH_URL
        employee_list = self.get_company_id
        for num in range(len(employee_list)):
            params = {
                "employer_id": employee_list[num],
                "per_page": 100,
                "only_with_salary": True,
                "area": self.get_city_id
            }
            response = requests.get(hh_vac_url, params=params)
            if response.status_code == 200:
                vacancies = response.json()
                for item in vacancies["items"]:
                    if item["salary"]["from"]:
                        vacancies_list.append(item)

        for vacancy in vacancies_list:
            shorten_vacancy = {
                "name_company": vacancy['employer']['name'],
                "vacancy_id": int(vacancy['id']),
                "company_id": vacancy['employer']['id'],
                "name_vacancy": vacancy['name'],
                "salary_from": vacancy['salary']['from'],
                "city": vacancy['area']['name'],
                "url_vacancy": vacancy['alternate_url'],
                "schedule": vacancy['schedule']['name'],
                "experience": vacancy['experience']['name'],
                "url_company": vacancy['employer']['alternate_url'],
            }
            vacancies_shorten.append(shorten_vacancy)

        return vacancies_shorten