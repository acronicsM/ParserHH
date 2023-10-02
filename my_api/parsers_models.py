from abc import ABC, abstractmethod
import time
from datetime import datetime
from bs4 import BeautifulSoup
import re

from my_api import db, app
from my_api.utils.common import get_json_data, delete_expired_vacancies, update_statistics
from my_api.parsers.currency_exchange_rate_parser import current_course
from my_api.models import Skills, Vacancy, SkillsVacancy, Query


class Parser(ABC):
    @abstractmethod
    def update_vacancy(self, query: str | Query):
        pass

    @classmethod
    def save_vacancy_from_db(cls, query: str | Query, data_json: dict, courses: dict | None = None) -> tuple[int, int]:
        vacancies_processed = new_vacancies = 0

        for v in data_json['items']:
            vacancies_processed += 1
            vacancy = Vacancy.query.get(vac_id := v['id'])
            if vacancy:
                vacancy.relevance_date = datetime.utcnow()
            else:
                new_vacancies += 1
                vacancy = Vacancy(id=vac_id, name=v['name'])
                vacancy.parser_raw_json(raw_json=v, courses=courses)

                if isinstance(query, Query):
                    vacancy.querys.append(query)

            db.session.add(vacancy)
            # db.session.flush()
            db.session.commit()

        return vacancies_processed, new_vacancies

    @classmethod
    def update_detail_vacancy(cls, vacancy: Vacancy, detail_data: dict):
        def add_skill(skills_json, name_attr, vac: Vacancy):
            for skill_name in skills_json:
                skill = Skills.query.filter_by(name=skill_name).first()
                if not skill:
                    skill = Skills(name=skill_name)
                    db.session.add(skill)
                    db.session.commit()

                skill_vacancy = SkillsVacancy.query.filter_by(skill_id=skill.id, vacancy_id=vac.id).first()
                if not skill_vacancy:
                    skill_vacancy = SkillsVacancy(skill_id=skill.id, vacancy_id=vac.id)
                    db.session.add(skill_vacancy)
                    db.session.commit()

                setattr(skill_vacancy, name_attr, True)

        add_skill(skills_json=detail_data['key_skills'], name_attr='key_skill', vac=vacancy)
        add_skill(skills_json=detail_data['description_skills'], name_attr='description_skill', vac=vacancy)
        add_skill(skills_json=detail_data['basic_skills'], name_attr='basic_skill', vac=vacancy)

        vacancy.schedule = detail_data['schedule']
        vacancy.description = detail_data['description']
        vacancy.need_update = False

        db.session.add(vacancy)
        # db.session.flush()
        db.session.commit()


class HH(Parser):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    def update_vacancy(self, query: str | Query) -> dict:
        page, vacancies_processed, new_vacancies = self.__pages_loader(query_vac=query)
        delete_vacancies = delete_expired_vacancies()
        updated_details = self.__update_detail()

        update_statistics()

        return {
            'total_pages': page - 1,
            'vacancies_processed': vacancies_processed,
            'new_vacancies': new_vacancies,
            'remotely_vacancies': delete_vacancies,
            'updated_details': updated_details,
        }

    @staticmethod
    def __load_page(query: str | Query, per_page: int = 100, page: int = 0, courses=None, ) -> tuple[int, int]:

        query_str = query.name if isinstance(query, Query) else query

        params = {
            'text': query_str,
            'per_page': per_page,
            'search_field': 'name',
            'page': page,
        }

        return Parser.save_vacancy_from_db(data_json=get_json_data(params=params), courses=courses, query=query)

    def __pages_loader(self, query_vac: str, per_page: int = 100) -> tuple[int, int, int]:

        courses = current_course()

        page = vacancies_processed = new_vacancies = 0
        while True:
            processed, new = self.__load_page(query=query_vac, per_page=per_page, page=page, courses=courses)
            new_vacancies += new
            vacancies_processed += processed
            page += 1

            if processed == 0:
                break

        return page, vacancies_processed, new_vacancies

    def __update_detail(self) -> int:
        counter = 0
        timeout = app.config['TIMEOUT_DETAIL_LOADER']

        for vacancy in Vacancy.query.filter(Vacancy.need_update).all():
            counter += 1

            data_json = get_json_data(uri=str(vacancy.id))

            if data_json is None:
                continue

            super().update_detail_vacancy(vacancy, self.__parse_detail_data(data_json))

            if counter % app.config['PACKAGE_DETAIL_LOADER'] == 0:
                time.sleep(timeout)
                timeout += app.config['DELTA_DETAIL_LOADER']

        return counter

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


class Habr(ABC):
    pass
