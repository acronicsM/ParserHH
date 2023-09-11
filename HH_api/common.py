from datetime import datetime
import pickle
from pathlib import Path

import requests
from requests.compat import urljoin

from environment import VACANCY_FOLDER, BASE_URI, HEADER


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

    return requests.get(url=urljoin(BASE_URI, uri), params=params, headers=header).json()


def save_vacancy(vacancy):
    exists_and_makedir(VACANCY_FOLDER)

    with open(fr'{VACANCY_FOLDER}\{vacancy.vac_id}.bin', 'wb') as fp:
        pickle.dump(vacancy, fp)
