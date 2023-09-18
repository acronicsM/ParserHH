import time
from ..common import get_json_data, delete_expired_vacancies
from ..parsers.api_parser import parse_detail_data
from ..parsers.currency_exchange_rate_parser import current_course
from .. import db
from ..models import Skills, Vacancy, Query
from datetime import datetime


def load_page(query: str | Query, per_page: int = 100, page: int = 0, courses=None) -> tuple[int, int]:

    query_str = query.name if isinstance(query, Query) else query

    params = {
        'text': query_str,
        'per_page': per_page,
        'search_field': 'name',
        'page': page,
    }

    save_vacancy_from_db(data_json=get_json_data(params=params), courses=courses, query=query)

    return 0, 0


def pages_loader(query_vac: str, per_page: int = 100):

    courses = current_course()

    vacancies_processed = 0
    total_vacancies = 1
    page = 0

    while vacancies_processed < total_vacancies:
        _total_vacancies, _vacancies_processed = load_page(query=query_vac,
                                                           per_page=per_page,
                                                           page=page,
                                                           courses=courses
                                                           )
        total_vacancies = _total_vacancies
        vacancies_processed += _vacancies_processed
        page += 1

    return vacancies_processed, total_vacancies


def update_detail():
    counter = 0
    timeout = 5
    delta = 2
    package = 5
    for vacancy in Vacancy.query.filter(Vacancy.need_update).all():
        counter += 1

        data_json = get_json_data(uri=str(vacancy.id))

        if data_json is None:
            continue

        update_detail_vacancy(vacancy, parse_detail_data(data_json))

        if counter % package == 0:
            time.sleep(timeout)
            timeout += delta


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


def save_vacancy_from_db(query: str | Query, data_json: dict, courses: dict | None = None) -> None:
    for v in data_json['items']:
        vacancy = Vacancy.query.get(vac_id := v['id'])
        if vacancy:
            vacancy.relevance_date = datetime.utcnow()
        else:
            vacancy = Vacancy(id=vac_id, name=v['name'])
            vacancy.parser_raw_json(raw_json=v, courses=courses)

            if isinstance(query, Query):
                vacancy.querys.append(query)

        db.session.add(vacancy)
        # db.session.flush()
        db.session.commit()


def update_vacancy(query: str | Query):
    pages_loader(query_vac=query)
    delete_expired_vacancies()
    update_detail()
