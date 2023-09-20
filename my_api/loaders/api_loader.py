import time
from datetime import datetime
from ..common import get_json_data, delete_expired_vacancies
from ..parsers.api_parser import parse_detail_data
from ..parsers.currency_exchange_rate_parser import current_course
from .. import db
from ..models import Skills, Vacancy, Query
from config import TIMEOUT_DETAIL_LOADER, DELTA_DETAIL_LOADER, PACKAGE_DETAIL_LOADER


def load_page(query: str | Query, per_page: int = 100, page: int = 0, courses=None, ) -> tuple[int, int]:

    query_str = query.name if isinstance(query, Query) else query

    params = {
        'text': query_str,
        'per_page': per_page,
        'search_field': 'name',
        'page': page,
    }

    return save_vacancy_from_db(data_json=get_json_data(params=params), courses=courses, query=query)


def save_vacancy_from_db(query: str | Query, data_json: dict, courses: dict | None = None) -> tuple[int, int]:
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


def pages_loader(query_vac: str, per_page: int = 100) -> tuple[int, int, int]:

    courses = current_course()

    page = vacancies_processed = new_vacancies = 0
    while True:
        processed, new = load_page(query=query_vac, per_page=per_page, page=page, courses=courses)
        new_vacancies += new
        vacancies_processed += processed
        page += 1

        if processed == 0:
            break

    return page, vacancies_processed, new_vacancies


def update_detail() -> int:
    counter = 0
    timeout = TIMEOUT_DETAIL_LOADER

    for vacancy in Vacancy.query.filter(Vacancy.need_update).all():
        counter += 1

        data_json = get_json_data(uri=str(vacancy.id))

        if data_json is None:
            continue

        update_detail_vacancy(vacancy, parse_detail_data(data_json))

        if counter % PACKAGE_DETAIL_LOADER == 0:
            time.sleep(timeout)
            timeout += DELTA_DETAIL_LOADER

    return counter


def update_detail_vacancy(vacancy: Vacancy, detail_data: dict):
    def add_skill_to_dict(skills_dict, skills_json, name_attr):
        for skill in skills_json:
            if skill not in skills_dict:
                skills_dict[skill] = Skills(name=skill)

            setattr(skills_dict[skill], name_attr, True)

    vacancy.schedule = detail_data['schedule']
    vacancy.description = detail_data['description']
    vacancy.need_update = False

    skills = dict()

    add_skill_to_dict(skills_dict=skills, skills_json=detail_data['key_skills'], name_attr='key_skill')
    add_skill_to_dict(skills_dict=skills, skills_json=detail_data['description_skills'], name_attr='description_skill')
    add_skill_to_dict(skills_dict=skills, skills_json=detail_data['basic_skills'], name_attr='basic_skill')

    vacancy.skills = list(skills.values())

    db.session.add(vacancy)
    # db.session.flush()
    db.session.commit()


def update_vacancy(query: str | Query) -> dict:

    page, vacancies_processed, new_vacancies = pages_loader(query_vac=query)
    delete_vacancies = delete_expired_vacancies()
    updated_details = update_detail()

    return {
        'total_pages': page - 1,
        'vacancies_processed': vacancies_processed,
        'new_vacancies': new_vacancies,
        'remotely_vacancies': delete_vacancies,
        'updated_details': updated_details,
    }
