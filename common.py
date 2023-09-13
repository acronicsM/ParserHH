from datetime import datetime, timedelta
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
                 'requirement',
                 'responsibility',
                 'experience',
                 'employment',
                 'description',
                 'key_skills',  # cкилы из тега key_skills
                 'description_skills',  # cкилы из тега description
                 'basic_skills',  # основные скилы вакансии
                 'schedule',
                 'need_update',
                 'relevance_date',
                 'currency',
                 )

    def __init__(self, vac_id: int, name: str, raw_json: str = None, courses: dict | None = None):
        self.vac_id, self.name = vac_id, name
        self.salary_from = self.salary_to = 0
        self.type = self.requirement = self.responsibility = self.experience = self.employment = self.description = ''
        self.key_skills = self.description_skills = self.basic_skills = set()
        self.schedule = ''
        self.published_at = None
        self.need_update = True
        self.relevance_date = datetime.now()

        if raw_json:
            self.__parser_raw_json(raw_json, courses)

    def __parser_raw_json(self, raw_json, courses):
        published_at = raw_json['published_at']
        published_at = published_at[:published_at.find('+')]

        self.type = raw_json['type']['name']
        self.published_at = datetime.fromisoformat(published_at)
        self.requirement = raw_json['snippet']['requirement']
        self.responsibility = raw_json['snippet']['responsibility']
        self.experience = raw_json['experience']['name']
        self.employment = raw_json['employment']['name']

        if raw_json['salary']:
            self.currency = raw_json['salary']['currency']
            self.salary_from = raw_json['salary']['from'] if raw_json['salary']['from'] else 0
            self.salary_to = raw_json['salary']['to'] if raw_json['salary']['to'] else 0
        else:
            self.currency = 'RUB'
            self.salary_from = 0
            self.salary_to = 0

        if courses:
            course = courses[self.currency]
            if not course:
                print(f'Не удалось конвертировать валюту {self.currency}')
            else:
                self.salary_from = self.salary_from * course
                self.salary_to = self.salary_to * course

    def save(self):
        exists_and_makedir(VACANCY_FOLDER)

        with open(fr'{VACANCY_FOLDER}\{self.vac_id}.bin', 'wb') as fp:
            pickle.dump(self, fp)


def exists_and_makedir(path: str):
    Path(path).mkdir(parents=True, exist_ok=True)


def get_json_data(params: dict = None, header: dict = None, uri: str = None):

    if not header:
        header = HEADER

    return requests.get(url=(BASE_URI + f'/{uri}/') if uri else BASE_URI, params=params, headers=header).json()


def get_vacancies_file():
    return Path(VACANCY_FOLDER).glob('[0-9]*.bin')


def get_vacancy_obj(path: str) -> Vacancy | None:
    with open(path, 'rb') as fp:
        return pickle.load(fp)


def get_dump_files(pattern: str):
    return Path(DUMPS_FOLDER).glob(pattern)


def get_vacancy_for_update_bin():
    vacancies_for_update = []
    for path in get_vacancies_file():
        vacancy = get_vacancy_obj(path)
        if vacancy.need_update:
            vacancies_for_update.append(vacancy)

    return vacancies_for_update


def save_vacancy_from_json(data_json: dict, courses: dict | None = None) -> None:
    for v in data_json['items']:
        vac_id = v['id']
        vacancy = None
        for path in Path(VACANCY_FOLDER).glob(f'{vac_id}.bin'):
            vacancy = get_vacancy_obj(path)
            vacancy.relevance_date = datetime.now()

        if vacancy is None:
            vacancy = Vacancy(vac_id=vac_id, name=v['name'], raw_json=v, courses=courses)

        vacancy.save()


def update_detail_vacancy(vacancy: Vacancy, detail_data: dict):
    vacancy.schedule = detail_data['schedule']
    vacancy.description = detail_data['description']
    vacancy.key_skills = detail_data['key_skills']
    vacancy.description_skills = detail_data['description_skills']
    vacancy.basic_skills = detail_data['basic_skills']
    vacancy.need_update = False


def get_all_vacancies():
    return [get_vacancy_obj(path) for path in get_vacancies_file()]


def delete_expired_vacancies(logging: bool = False):
    now_minus_1 = datetime.now() - timedelta(days=1)

    for vacancy in get_all_vacancies():
        if vacancy.relevance_date < now_minus_1:
            file = Path(fr'{VACANCY_FOLDER}\{vacancy.vac_id}.bin')
            file.unlink()

            if logging:
                print(f'Удалена вакансия {vacancy.vac_id}')
