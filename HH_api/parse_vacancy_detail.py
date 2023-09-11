from common import Vacancy, VACANCY_FOLDER, get_json_data, save_vacancy
from environment import DETAIL_FILENAME, DUMPS_FOLDER, DO_DUMP, REQUIRED_SKILLS

import json
import pickle
from bs4 import BeautifulSoup
import re
from pathlib import Path


def parser_description_to_key_skills(description: str):
    pattern = r'[a-zA-Z]{1,}[ -]?[a-zA-Z]{1,}'

    description_skills = set()
    basic_skills = set()

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


def get_detail_vacancy(vac_id: int, folder: str = None, do_dump: bool = None):
    if not folder:
        folder = DUMPS_FOLDER

    if do_dump is None:
        do_dump = DO_DUMP

    data_json = get_json_data(uri=str(vac_id))

    if do_dump:
        with open(fr'{folder}\{DETAIL_FILENAME}{vac_id}.json', 'w') as fp:
            json.dump(data_json, fp)

    return data_json


def parse_detail_data(vacancy: Vacancy, data_json: dict):
    vacancy.schedule = data_json['schedule']['name']
    vacancy.description = data_json['description']

    if data_json['key_skills']:
        vacancy.key_skills = {i['name'] for i in data_json['key_skills']}

    description_skills, basic_skills = parser_description_to_key_skills(vacancy.description)

    vacancy.description_skills, vacancy.basic_skills = description_skills, basic_skills


def update_detail_vacancy():
    for path in Path(VACANCY_FOLDER).glob('[0-9]*.bin'):
        with open(path, 'rb') as fp:
            vacancy: Vacancy = pickle.load(fp)
            data_json = get_detail_vacancy(vacancy.vac_id)

            parse_detail_data(vacancy=vacancy, data_json=data_json)

            save_vacancy(vacancy=vacancy)


if __name__ == '__main__':
    update_detail_vacancy()
