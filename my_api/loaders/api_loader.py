import time
from datetime import datetime
from my_api.utils.common import get_json_data, delete_expired_vacancies
from my_api.parsers.api_parser import parse_detail_data
from my_api.parsers.currency_exchange_rate_parser import current_course
from my_api import db, app
from my_api.models import Skills, Vacancy, SkillsVacancy, Query


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
    timeout = app.config['TIMEOUT_DETAIL_LOADER']

    for vacancy in Vacancy.query.filter(Vacancy.need_update).all():
        counter += 1

        data_json = get_json_data(uri=str(vacancy.id))

        if data_json is None:
            continue

        update_detail_vacancy(vacancy, parse_detail_data(data_json))

        if counter % app.config['PACKAGE_DETAIL_LOADER'] == 0:
            time.sleep(timeout)
            timeout += app.config['DELTA_DETAIL_LOADER']

    return counter


def update_detail_vacancy(vacancy: Vacancy, detail_data: dict):
    def add_skill(skills_json, name_attr, vacancy: Vacancy):
        for skill_name in skills_json:
            skill = Skills.query.filter_by(name=skill_name).first()
            if not skill:
                skill = Skills(name=skill_name)
                db.session.add(skill)
                db.session.commit()

            skill_vacancy = SkillsVacancy.query.filter_by(skill_id=skill.id, vacancy_id=vacancy.id).first()
            if not skill_vacancy:
                skill_vacancy = SkillsVacancy(skill_id=skill.id, vacancy_id=vacancy.id)
                db.session.add(skill_vacancy)
                db.session.commit()

            setattr(skill_vacancy, name_attr, True)

    add_skill(skills_json=detail_data['key_skills'], name_attr='key_skill', vacancy=vacancy)
    add_skill(skills_json=detail_data['description_skills'], name_attr='description_skill', vacancy=vacancy)
    add_skill(skills_json=detail_data['basic_skills'], name_attr='basic_skill', vacancy=vacancy)

    vacancy.schedule = detail_data['schedule']
    vacancy.description = detail_data['description']
    vacancy.need_update = False

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
