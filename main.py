from list_of_vacancies.HH_load_vacancies_list_API import load_vacancies
from list_of_vacancies.HH_parser_vacancies_list_API import hh_list_parser_and_dump, Vacancy

import requests
import json
import pickle


def filling_vacancies(vacancies: list[Vacancy], header: dict = None, dump_folder: str = '.', do_dump: bool = True):

    uri = 'https://api.hh.ru/vacancies'

    if not header:
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.0 (Edition Yx 05)'}

    for i in vacancies:
        raw_json = requests.get(f'{uri}/{i.vac_id}', headers=header).json()

        if do_dump:
            with open(fr'{dump_folder}\{i.vac_id}.json', 'w') as fp:
                json.dump(raw_json, fp)


def load_vacancies_class(filename: str) -> list[Vacancy]:
    vacancies = []
    with open(f'{filename}.bin', "rb") as fp:
        vac_class: Vacancy = pickle.load(fp)
        vacancies.append(vac_class)

    return vacancies


def filling_vacancies_class(vacancies: list[Vacancy]):
    pass


if __name__ == '__main__':

    query = 'Python junior'
    folder = 'dumps'
    pattern = 'hh[0-9]*.json'
    filename = 'Vacancy_class'

    # vac_processed, total_vac = load_vacancies(query=query, folder=folder)
    # print(f'Получено {vac_processed} вакансия из {total_vac}')

    # vacs = hh_list_parser_and_dump(folder=folder, pattern=pattern, filename=filename)
    #
    # filling_vacancies(vacancies=vacs, dump_folder=folder)

    vacs = load_vacancies_class(filename=filename)



