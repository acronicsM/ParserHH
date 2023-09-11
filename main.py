from parse_vacancies_list import load_vacancies


if __name__ == '__main__':

    query = 'Python junior'

    vac_processed, total_vac = load_vacancies(query=query)
    print(f'Получено {vac_processed} вакансия из {total_vac}')





