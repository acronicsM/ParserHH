
from list_of_vacancies.HH_load_vacancies_list_API import load_vacancies
from list_of_vacancies.HH_parser_vacancies_list_API import hh_list_parser_and_dump, Vacancy, dump_vacancys_list

import requests
import json
import pickle
from bs4 import BeautifulSoup
import os


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


def load_vacancies_class(filename: str, folder: str = '.') -> list:
    with open(fr'{folder}\{filename}.bin', "rb") as fp:
        return pickle.load(fp)

    return []


def get_json_from_dump(vac_id: int, folder: str = '.') -> dict|None:
    full_path = fr'{folder}\{vac_id}.json'
    if os.path.exists(full_path):
        with open(full_path, 'r') as fp:
            data = json.load(fp)
            return data

    return None


def filling_vacancies_class(vacancies: list[Vacancy], folder: str = '.'):
    for vac in vacancies:
        vac_data = get_json_from_dump(vac_id=vac.vac_id, folder=folder)
        vac.schedule = vac_data['schedule']['name']
        vac.description = vac_data['description']
        if vac_data['key_skills']:
            vac.key_skills = [i['name'] for i in vac_data['key_skills']]


def parser_description_to_key_skills(vacancies: list[Vacancy]):
    for vac in vacancies:
        soup = BeautifulSoup(vac.description, "html.parser")
        soup.text



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

    # vacs = load_vacancies_class(filename=filename, folder=folder)
    # filling_vacancies_class(vacancies=vacs, folder=folder)
    # dump_vacancys_list(vacancies=vacs, folder=folder, filename=filename)

    vacs = load_vacancies_class(filename=filename, folder=folder)
    parser_description_to_key_skills(vacancies=vacs)





