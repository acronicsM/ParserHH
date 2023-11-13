from abc import ABC, abstractmethod
import time
from datetime import datetime
from bs4 import BeautifulSoup
import re
import requests

from . import db, app, logging
from .utils.sql_queries import flush
from .models import Skills, Vacancy, SkillsVacancy, Query

glossary = app.config['GLOSSARY']
PACKAGE_DETAIL_LOADER = app.config['PACKAGE_DETAIL_LOADER']
TIMEOUT_DETAIL_LOADER = app.config['TIMEOUT_DETAIL_LOADER']
REQUIRED_SKILLS = app.config['REQUIRED_SKILLS']
HEADER = app.config['HEADER']


def get_json_data(uri: str, params: dict = None, header: dict = None):
    response = requests.get(
        url=uri,
        params=params,
        headers=HEADER if not header else header,
    ).json()

    logging.info(f'Response to {uri} with the {params} parameter ::: {response}')

    return response


class Singleton:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance


class Parser(ABC):
    @abstractmethod
    def update_vacancy(self, query: str | Query):
        pass

    @abstractmethod
    def get_detail_vacancy(self, vacancy_id: int):
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
    URI_BASE = 'https://hh.ru/vacancy'
    URI = 'https://api.hh.ru/vacancies'

    def update_vacancy(self, query: str | Query) -> dict:

        logging.info('Start of the job parser')

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

        logging.info('Completing the Job Parser')

        return result

    def __load_page(self, query: str | Query, per_page: int = 100, page: int = 0, courses=None, ) -> tuple[int, int]:

        query_str = query.name if isinstance(query, Query) else query

        params = {
            'text': query_str,
            'per_page': per_page,
            'search_field': 'name',
            'page': page,
        }

        logging.info(f'Page loading {self.URI} with parameters {params}')

        return self.save_vacancy_from_db(
            data_json=get_json_data(
                uri=self.URI,
                params=params,
            ),
            courses=courses,
            query=query,
        )

    def save_vacancy_from_db(self, query: str | Query, data_json: dict, courses: dict | None = None) -> tuple[int, int]:
        def parser_raw_json(vac_model, raw_json, crs):
            published_at = raw_json['published_at']
            published_at = published_at[:published_at.find('+')]

            vac_model.relevance_date = datetime.utcnow()
            vac_model.need_update = True

            vac_model.type = raw_json['type']['name']
            vac_model.published_at = datetime.fromisoformat(published_at)
            vac_model.requirement = raw_json['snippet']['requirement']
            vac_model.responsibility = raw_json['snippet']['responsibility']
            vac_model.experience = raw_json['experience']['name']
            vac_model.employment = raw_json['employment']['name']

            if raw_json['salary']:
                vac_model.currency = raw_json['salary']['currency']
                vac_model.salary_from = raw_json['salary']['from'] if raw_json['salary']['from'] else 0
                vac_model.salary_to = raw_json['salary']['to'] if raw_json['salary']['to'] else 0
            else:
                vac_model.currency = 'RUB'
                vac_model.salary_from = 0
                vac_model.salary_to = 0

            if crs and crs[vac_model.currency]:
                vac_model.salary_from = vac_model.salary_from * crs[vac_model.currency]
                vac_model.salary_to = vac_model.salary_to * crs[vac_model.currency]

        vacancies_processed = new_vacancies = 0

        for v in data_json['items']:
            vacancies_processed += 1
            if vacancy := Vacancy.query.get(vac_id := v['id']):
                vacancy.relevance_date = datetime.utcnow()
            else:
                new_vacancies += 1
                vacancy = Vacancy(id=vac_id, name=v['name'], url=f'{self.URI_BASE}/{vac_id}')
                parser_raw_json(vac_model=vacancy, raw_json=v, crs=courses)

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

    def get_detail_vacancy(self, vacancy_id: int):
        return self.__parse_detail_data(
            data_json=get_json_data(
                uri=f'{self.URI}/{vacancy_id}',
            )
        )

    def __update_detail(self) -> tuple[int, bool]:
        counter, error, timeout = 0, True, TIMEOUT_DETAIL_LOADER

        for vacancy in Vacancy.query.filter(Vacancy.need_update).all():
            counter += 1

            detail_vacancy = self.get_detail_vacancy(vacancy.id)

            if error := super().update_detail_vacancy(vacancy, detail_vacancy):
                return 0, error

            if counter % PACKAGE_DETAIL_LOADER == 0:
                time.sleep(timeout)
                timeout += PACKAGE_DETAIL_LOADER

        return counter, not flush()

    @staticmethod
    def parser_description_to_key_skills(description: str):
        pattern = r'[a-zA-Z]{1,}[ -]?[a-zA-Z]{1,}'

        description_skills = set()
        basic_skills = set()
        required_skills = REQUIRED_SKILLS

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

    def __parse_detail_data(self, data_json: dict | None):

        if not data_json or 'errors' in data_json:
            return None

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
