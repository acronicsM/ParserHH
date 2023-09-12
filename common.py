from datetime import datetime
import pickle
from pathlib import Path


import requests

from environment import VACANCY_FOLDER, BASE_URI, HEADER, DUMPS_FOLDER


class Vacancy:
    __slots__ = ('vac_id',
                 'name',
                 'salary_from',
                 'salary_to',
                 'type',
                 'published_at',
                 'archived',
                 'requirement',
                 'responsibility',
                 'experience',
                 'employment',
                 'description',
                 'key_skills',  # cкилы из тега key_skills
                 'description_skills',  # cкилы из тега description
                 'basic_skills',  # основные скилы вакансии
                 'schedule')

    def __init__(self, vac_id: int, name: str, raw_json: str = None):
        self.vac_id, self.name = vac_id, name
        self.salary_from = self.salary_to = 0
        self.type = self.requirement = self.responsibility = self.experience = self.employment = self.description = ''
        self.key_skills = self.description_skills = self.basic_skills = set()
        self.schedule = ''
        self.published_at = None
        self.archived = False

        if raw_json:
            self.__parser_raw_json(raw_json)

    def __parser_raw_json(self, raw_json):
        self.salary_from = raw_json['salary']['from'] if raw_json['salary'] else None
        self.salary_to = raw_json['salary']['to'] if raw_json['salary'] else None
        self.type = raw_json['type']['name']
        self.published_at = datetime.fromisoformat(raw_json['published_at'])
        self.archived = raw_json['archived']
        self.requirement = raw_json['snippet']['requirement']
        self.responsibility = raw_json['snippet']['responsibility']
        self.experience = raw_json['experience']['name']
        self.employment = raw_json['employment']['name']


def exists_and_makedir(path: str):
    Path(path).mkdir(parents=True, exist_ok=True)


def get_json_data(params: dict = None, header: dict = None, uri: str = None):

    if not header:
        header = HEADER

    return requests.get(url=(BASE_URI + f'/{uri}/') if uri else BASE_URI, params=params, headers=header).json()


def save_vacancy(vacancy):
    exists_and_makedir(VACANCY_FOLDER)

    with open(fr'{VACANCY_FOLDER}\{vacancy.vac_id}.bin', 'wb') as fp:
        pickle.dump(vacancy, fp)


def get_vacancies_file():
    return Path(VACANCY_FOLDER).glob('[0-9]*.bin')


def get_vacancy_obj(path: str) -> Vacancy|None:
    with open(path, 'rb') as fp:
        return pickle.load(fp)


def get_dump_files(pattern: str):
    return Path(DUMPS_FOLDER).glob(pattern)

