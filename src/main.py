import psycopg2
from pprint import pprint
from config import config
from class_api_hh import HeadhunterVacancy
from DBManager import DBManager, CreateDatabase


def main():
    """Функция интерфейса для пользователя"""
    db_name = 'employer_vacancy'
    table_name = 'employer'
    params = config()
    conn = None

    print('Вас приветствует программа сбора вакансий с платформы HeadHunter.')
    print('---------------------------------------------')
    area_input = input('Укажите в каком городе будем искать вакансии,\n'
                    'если по всей стране, напишите "Россия": ').capitalize()
    print('---------------------------------------------')
    instance_hh = HeadhunterVacancy(area_input)

    print('По умолчанию заданы 10 компаний работодателей по которым собираем вакансии:')
    instance_hh = HeadhunterVacancy(area_input)  # Экземпляр класса HeadhunterVacancy
    company_nam = instance_hh.company_name
    for company in company_nam:
        print(company)

    created = CreateDatabase()  # Экземпляр класса CreateDatabase
    created.create_database(params, db_name)
    print('---------------------------------------------')
    print(f"БД {db_name} успешно создана")
    print('---------------------------------------------')
    params.update({'dbname': db_name})

    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:

                created.create_table(cur)
                print(f"Таблица employer успешно создана")
                print('---------------------------------------------')
                add_data = instance_hh.get_vacancies()

                created.add_data_to_table(cur, add_data)
                print(f"Таблица employer успешно заполнена")
                print(f'Всего найдено вакансий: {len(add_data)}, по географическому указанию: {area_input}')
                print('---------------------------------------------')
                while True:
                    instance_dbmanager = DBManager(params)  # Экземпляр класса DBManager
                    user_input = input('Возможности работы с базой данных:\n'
                                       '1 - Вывести список всех компаний и количество вакансий у каждой компании.\n'
                                       '2 - Вывести список всех вакансий с указанием названия компании, '
                                       'названия вакансии, зарплаты и ссылки на вакансию.\n'
                                       '3 - Вывести среднюю зарплату по всем вакансиям.\n'
                                       '4 - Вывести список всех вакансий, у которых зарплата, '
                                       'выше средней по всем вакансиям.\n'
                                       '5 - Вывести список всех вакансий, в названии которых содержатся, '
                                       'переданные в метод слова, например “python”.\n'
                                       '6 - Вывести данные о работодателях.\n'
                                       '7 - Выход из программы.\n-----> ')

                    if user_input not in ('1', '2', '3', '4', '5', '6', '7'):
                        print('Введите корректный ответ')

                    # Выход
                    elif user_input == '7':
                        break

                    elif user_input == '1':
                        data = instance_dbmanager.get_companies_and_vacancies_count(cur)
                        print(*data, sep='\n')

                    elif user_input == '2':
                        data = instance_dbmanager.get_all_vacancies(cur)
                        print(*data, sep='\n')

                    elif user_input == '3':
                        data = instance_dbmanager.get_avg_salary(cur)[0]
                        print(*data, sep='\n')

                    elif user_input == '4':
                        data = instance_dbmanager.get_vacancies_with_higher_salary(cur)
                        print(*data, sep='\n')

                    elif user_input == '5':
                        keyword = input('Введите ключевое слово для поиска в названии вакансии -> ').capitalize()
                        data = instance_dbmanager.get_vacancies_with_keyword(keyword, cur)
                        if data:
                            print(*data, sep='\n')
                        else:
                            print('По введенному ключевому слову вакансий не найдено(')

                    elif user_input == '6':
                        data = instance_hh.company_information()
                        for item in data:
                            print('---------------------------------------------')
                            pprint(item, indent=2)

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    main()