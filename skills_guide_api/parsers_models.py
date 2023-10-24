from abc import ABC, abstractmethod
import time
from datetime import datetime
from bs4 import BeautifulSoup
import re
import requests

from . import db, app
from .utils.sql_queries import flush
from .models import Skills, Vacancy, SkillsVacancy, Query

glossary = app.config['GLOSSARY']


def get_json_data(params: dict = None, header: dict = None, uri: str = None):
    if not header:
        header = app.config['HEADER']

    url = (app.config['BASE_URI'] + f'/{uri}/') if uri else app.config['BASE_URI']

    response = requests.get(url=url, params=params, headers=header).json()
    return response


def hh_parser_raw_json(vacancy, raw_json, courses):
    published_at = raw_json['published_at']
    published_at = published_at[:published_at.find('+')]

    vacancy.relevance_date = datetime.utcnow()
    vacancy.need_update = True

    vacancy.type = raw_json['type']['name']
    vacancy.published_at = datetime.fromisoformat(published_at)
    vacancy.requirement = raw_json['snippet']['requirement']
    vacancy.responsibility = raw_json['snippet']['responsibility']
    vacancy.experience = raw_json['experience']['name']
    vacancy.employment = raw_json['employment']['name']

    if raw_json['salary']:
        vacancy.currency = raw_json['salary']['currency']
        vacancy.salary_from = raw_json['salary']['from'] if raw_json['salary']['from'] else 0
        vacancy.salary_to = raw_json['salary']['to'] if raw_json['salary']['to'] else 0
    else:
        vacancy.currency = 'RUB'
        vacancy.salary_from = 0
        vacancy.salary_to = 0

    if courses:
        course = courses[vacancy.currency]
        if not course:
            print(f'Не удалось конвертировать валюту {vacancy.currency}')
        else:
            vacancy.salary_from = vacancy.salary_from * course
            vacancy.salary_to = vacancy.salary_to * course


class Singleton:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance


class Parser(ABC):
    @abstractmethod
    def update_vacancy(self, query: str | Query):
        pass

    @classmethod
    def update_detail_vacancy(cls, vacancy: Vacancy, detail_data: dict):
        def add_skill(skills_json, name_attr, vac: Vacancy):
            for skill_name in skills_json:
                skill = Skills.query.filter_by(name=skill_name).first()
                if not skill:
                    skill = Skills(name=skill_name)
                    db.session.add(skill)
                    if not flush():
                        return True

                skill_vacancy = SkillsVacancy.query.filter_by(skill_id=skill.id, vacancy_id=vac.id).first()
                if not skill_vacancy:
                    skill_vacancy = SkillsVacancy(skill_id=skill.id, vacancy_id=vac.id)
                    db.session.add(skill_vacancy)
                    if not flush():
                        return True

                setattr(skill_vacancy, name_attr, True)

                return False

        for i in glossary:
            error = add_skill(skills_json=detail_data[i], name_attr=i, vac=vacancy)

            if error:
                return True

        vacancy.schedule = detail_data['schedule']
        vacancy.description = detail_data['description']
        vacancy.need_update = False

        db.session.add(vacancy)

        return False


class HH(Singleton, Parser):
    def update_vacancy(self, query: str | Query) -> dict:

        result = {
            'total_pages': 0,
            'vacancies_processed': 0,
            'new_vacancies': 0,
            'remotely_vacancies': 0,
            'updated_details': 0,
            'error': True
        }

        page, vacancies_processed, new_vacancies, error_pages = self.__pages_loader(query_vac=query)

        if error_pages:
            return result

        updated_details, error_detail = self.__update_detail()

        result['total_pages'] = page - 1
        result['vacancies_processed'] = vacancies_processed
        result['new_vacancies'] = new_vacancies
        result['updated_details'] = updated_details
        result['error'] = error_detail

        return result

    def __load_page(self, query: str | Query, per_page: int = 100, page: int = 0, courses=None, ) -> tuple[int, int]:

        query_str = query.name if isinstance(query, Query) else query

        params = {
            'text': query_str,
            'per_page': per_page,
            'search_field': 'name',
            'page': page,
        }

        return self.save_vacancy_from_db(data_json=get_json_data(params=params), courses=courses, query=query)

    @staticmethod
    def save_vacancy_from_db(query: str | Query, data_json: dict, courses: dict | None = None) -> tuple[int, int]:
        vacancies_processed = new_vacancies = 0

        for v in data_json['items']:
            vacancies_processed += 1
            if vacancy := Vacancy.query.get(vac_id := v['id']):
                vacancy.relevance_date = datetime.utcnow()
            else:
                new_vacancies += 1
                vacancy = Vacancy(id=vac_id, name=v['name'], url=f'https://hh.ru/vacancy/{vac_id}')
                hh_parser_raw_json(vacancy=vacancy, raw_json=v, courses=courses)

                if isinstance(query, Query):
                    vacancy.querys.append(query)

            db.session.add(vacancy)

        return vacancies_processed, new_vacancies

    def __pages_loader(self, query_vac: str, per_page: int = 100) -> tuple[int, int, int, bool]:

        from .utils.currency_exchange_rate_parser import current_course
        courses = current_course()

        page = vacancies_processed = new_vacancies = 0
        while True:
            processed, new = self.__load_page(query=query_vac, per_page=per_page, page=page, courses=courses)
            new_vacancies += new
            vacancies_processed += processed
            page += 1

            if processed == 0:
                break

        return page, vacancies_processed, new_vacancies, not flush()

    def __update_detail(self) -> tuple[int, bool]:
        counter, error, timeout = 0, True, app.config['TIMEOUT_DETAIL_LOADER']

        for vacancy in Vacancy.query.filter(Vacancy.need_update).all():
            counter += 1

            data_json = get_json_data(uri=str(vacancy.id))

            if data_json is None:
                continue

            error = super().update_detail_vacancy(vacancy, self.__parse_detail_data(data_json))

            if error:
                return 0, error

            if counter % app.config['PACKAGE_DETAIL_LOADER'] == 0:
                time.sleep(timeout)
                timeout += app.config['DELTA_DETAIL_LOADER']

        return counter, not flush()

    @staticmethod
    def parser_description_to_key_skills(description: str):
        pattern = r'[a-zA-Z]{1,}[ -]?[a-zA-Z]{1,}'

        description_skills = set()
        basic_skills = set()
        required_skills = app.config['REQUIRED_SKILLS']

        soup = BeautifulSoup(description, 'html.parser')
        for ul in soup.findAll('ul'):
            name = ul.find_previous('p')
            if name is None:
                name = ul.find_previous('strong')

            name = name.text

            for child in ul.findChildren('li', recursive=False):
                for match in re.finditer(pattern, child.text, re.MULTILINE):
                    skill = match.group()
                    description_skills.add(skill)
                    if any((name.lower() in i.lower()) or (i.lower() in name.lower()) for i in required_skills):
                        basic_skills.add(skill)

        return description_skills, basic_skills

    def __parse_detail_data(self, data_json: dict):
        description_skills, basic_skills = self.parser_description_to_key_skills(data_json['description'])

        result = {
            'schedule': data_json['schedule']['name'],
            'description': data_json['description'],
            'key_skills': {i['name'] for i in data_json['key_skills']} if data_json['key_skills'] else set(),
            'description_skills': description_skills,
            'basic_skills': basic_skills,
            'need_update': False
        }

        return result


# class Habr(Singleton, ABC):
#     def update_vacancies(self, query: str | Query):
#         return None
