import json
import os
import re
from datetime import datetime
import pickle


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
                 'description_skills',   # cкилы из тега description
                 'basic_skills',  # основные скилы вакансии
                 'schedule')

    def __init__(self, vac_id: int, name: str):
        self.vac_id, self.name = vac_id, name
        self.key_skills = set()
        self.basic_skills = set()
        self.description_skills = set()
        self.description = ''


def hh_list_parser_and_dump(folder: str, pattern: str, filename: str) -> list:
    vacancies = []

    for f in os.listdir(folder):
        full_path = folder + '/' + f
        if not os.path.isfile(full_path) or re.fullmatch(pattern, f) is None:
            continue

        with open(full_path, 'r') as fp:
            for i in json.load(fp):
                new_vac = Vacancy(i['id'], i['name'])
                new_vac.salary_from = i['salary']['from'] if i['salary'] else None
                new_vac.salary_to = i['salary']['to'] if i['salary'] else None
                new_vac.type = i['type']['name']
                new_vac.published_at = datetime.fromisoformat(i['published_at'])
                new_vac.archived = i['archived']
                new_vac.requirement = i['snippet']['requirement']
                new_vac.responsibility = i['snippet']['responsibility']
                new_vac.experience = i['experience']['name']
                new_vac.employment = i['employment']['name']

                vacancies.append(new_vac)

    dump_vacancys_list(vacancies=vacancies, folder=folder, filename=filename)

    return vacancies


def dump_vacancys_list(vacancies: list[Vacancy], folder: str, filename: str):
    with open(fr'{folder}\{filename}.bin', 'wb') as fp:
        pickle.dump(vacancies, fp)
