import psycopg2


class CreateDatabase:
    """Класс создания базы данных, таблицы и ее заполнения"""
    def __init__(self):
        pass

    @staticmethod
    def create_database(params, db_name) -> None:
        """
        Функция создания базы данных
        """

        connection = psycopg2.connect(dbname='postgres', **params)
        connection.autocommit = True
        cursor = connection.cursor()

        cursor.execute(f"DROP DATABASE IF EXISTS {db_name};")
        cursor.execute(f"CREATE DATABASE {db_name};")

        cursor.close()
        connection.close()

    @staticmethod
    def create_table(cur) -> None:
        """
        Функция создания таблицы для ее последующего заполнения данными о вакансиях
        """
        cur.execute(
                """
                DROP TABLE IF EXISTS employer;
                CREATE TABLE employer(
                name_company varchar(50),
                vacancy_id int,
                company_id int,
                name_vacancy varchar(100),
                salary_from int,
                city varchar(50),
                url_vacancy character varying(50),
                schedule varchar(50),
                experience character varying(50),
                url_company character varying(50)
                )
                """
                )

    @staticmethod
    def add_data_to_table(cur, data: list[dict]) -> None:
        """
        Функция для заполнения таблицы базы данных
        """
        for vacancy in data:
            cur.execute("""
            INSERT INTO employer 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (vacancy['name_company'],
                    vacancy['vacancy_id'],
                    vacancy['company_id'],
                    vacancy['name_vacancy'],
                    vacancy['salary_from'],
                    vacancy['city'],
                    vacancy['url_vacancy'],
                    vacancy['schedule'],
                    vacancy['experience'],
                    vacancy['url_company']))


class DBManager:
    """Класс для подключения к базе данных и работе с вакансиями"""
    def __init__(self, params):
        self.params = params

    @staticmethod
    def get_companies_and_vacancies_count(cur):
        """Получает список всех компаний и количество вакансий у каждой компании"""
        cur.execute('SELECT name_company, count(*) FROM employer GROUP BY name_company')
        result = cur.fetchall()

        return result

    @staticmethod
    def get_all_vacancies(cur):
        """Получает список всех вакансий с указанием названия компании, названия вакансии
        и зарплаты и ссылки на вакансию"""
        cur.execute("""SELECT * FROM employer""")
        result = cur.fetchall()

        return result

    @staticmethod
    def get_avg_salary(cur):
        """Получает среднюю зарплату по вакансиям"""
        cur.execute("""SELECT AVG(salary_from) as average
                        FROM employer""")
        result = cur.fetchall()
        return result

    @staticmethod
    def get_vacancies_with_higher_salary(cur):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        cur.execute("""SELECT * FROM employer
                    WHERE salary_from > (SELECT AVG(salary_from) FROM employer)""")
        result = cur.fetchall()
        return result

    @staticmethod
    def get_vacancies_with_keyword(keyword, cur):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”"""
        cur.execute(f"SELECT * FROM employer WHERE name_vacancy LIKE '%{keyword}%'")
        result = cur.fetchall()
        return result