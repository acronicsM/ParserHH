import time

from common import Vacancy, get_json_data, save_vacancy, get_vacancies_file, get_vacancy_obj
from environment import DETAIL_FILENAME, DUMPS_FOLDER, DO_DUMP, REQUIRED_SKILLS

import json
from bs4 import BeautifulSoup
import re
from pathlib import Path


def parser_description_to_key_skills(description: str):
    pattern = r'[a-zA-Z]{1,}[ -]?[a-zA-Z]{1,}'

    description_skills = basic_skills = set()

    soup = BeautifulSoup(description, 'html.parser')
    for ul in soup.findAll('ul'):
        name = ul.find_previous('p')
        if name is None:
            name = ul.find_previous('strong')

        for child in ul.findChildren('li', recursive=False):
            for match in re.finditer(pattern, child.text, re.MULTILINE):
                skill = match.group()
                description_skills.add(skill)
                if name in REQUIRED_SKILLS:
                    basic_skills.add(skill)

    return description_skills, basic_skills


def parse_detail_data(vacancy: Vacancy, data_json: dict):
    vacancy.schedule = data_json['schedule']['name']
    vacancy.description = data_json['description']

    if data_json['key_skills']:
        vacancy.key_skills = {i['name'] for i in data_json['key_skills']}

    description_skills, basic_skills = parser_description_to_key_skills(vacancy.description)

    vacancy.description_skills, vacancy.basic_skills = description_skills, basic_skills


def get_detail_vacancy(vac_id: int, folder: str = None, do_dump: bool = None, from_dump: bool = None):
    if not folder:
        folder = DUMPS_FOLDER

    if from_dump:
        return get_detail_data_from_dump(vac_id, folder)

    if do_dump is None:
        do_dump = DO_DUMP

    data_json = get_json_data(uri=str(vac_id))

    if do_dump:
        with open(fr'{folder}\{DETAIL_FILENAME}{vac_id}.json', 'w') as fp:
            json.dump(data_json, fp)

    return data_json


def get_detail_data_from_dump(vac_id: int, folder: str):
    path = fr'{folder}\{DETAIL_FILENAME}{vac_id}.json'
    if not Path(path).exists():
        return

    with open(path, 'r') as fp:
        return json.load(fp)


def update_detail_vacancy(folder: str = None, do_dump: bool = None, from_dump: bool = None, logging: bool = False):
    counter = job_counter = 0
    paths = list(get_vacancies_file())
    for path in paths:
        job_counter += 1

        vacancy: Vacancy = get_vacancy_obj(path)

        if logging:
            print(f'Детальный парсинг вакансии {vacancy.vac_id} ({job_counter} из {len(paths)})')

        data_json = get_detail_vacancy(vac_id=vacancy.vac_id, folder=folder, do_dump=do_dump, from_dump=from_dump)

        if data_json is None:
            if logging:
                print(f'Не удалось получить детальные данные вакансии {vacancy.vac_id}')
            continue

        parse_detail_data(vacancy=vacancy, data_json=data_json)

        save_vacancy(vacancy=vacancy)

        counter += 1
        if counter == 3 and not from_dump:
            time.sleep(20)
            counter = 0


if __name__ == '__main__':
    update_detail_vacancy(from_dump=True, logging=True)
