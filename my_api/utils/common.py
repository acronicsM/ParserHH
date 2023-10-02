from datetime import datetime, timedelta
from pathlib import Path
import requests

from my_api.models import Vacancy, Skills, Query, Statistics, TopVacancies, TopSkills, Aggregator
from my_api import db, app

from . import querys


def exists_and_makedir(path: str):
    Path(path).mkdir(parents=True, exist_ok=True)


def get_json_data(params: dict = None, header: dict = None, uri: str = None):
    if not header:
        header = app.config['HEADER']

    url = (app.config['BASE_URI'] + f'/{uri}/') if uri else app.config['BASE_URI']

    return requests.get(url=url, params=params, headers=header).json()


def get_all_vacancies(page=0, per_page=10, tag_id=None, query_id=None):
    query = querys.all_vacancies(tag_id=tag_id, query_id=query_id)

    return query.count(), query.offset(page * per_page).limit(per_page).all()


def get_vacancy_by_id(vacancy_id):
    return db.session.get(Vacancy, vacancy_id)


def get_vacancy_skills(vacancy_id):
    vacancy = db.session.get(Vacancy, vacancy_id)
    if not vacancy:
        return []
    return [skill.to_dict() for skill in vacancy.skill_vacancies]


def get_skill_vacancies(skill_id):
    return [i.vacancy.to_dict() for i in Skills.query.get(skill_id).skill_vacancies]


def get_all_skills(page=0, per_page=10):
    skills_query = querys.all_skills()

    count = skills_query.count()

    skills_page = []
    for skill in skills_query.offset(page * per_page).limit(per_page).all():
        skills_page.append({
            'id': skill.id,
            'name': skill.name,
            'vacancies': len(skill.skill_vacancies),
            'key': sum(i.key_skill for i in skill.skill_vacancies),
            'description': sum(i.description_skill for i in skill.skill_vacancies),
            'basic': sum(i.basic_skill for i in skill.skill_vacancies),
        })

    return {'found': count, 'result': skills_page}


def delete_expired_vacancies() -> int:
    now_minus_1_day = datetime.now() - timedelta(days=1)
    delete_vacancies = 0

    for vacancy in get_all_vacancies()[1]:
        if vacancy.relevance_date < now_minus_1_day:
            db.session.delete(vacancy)
            delete_vacancies += 1

    return delete_vacancies


def get_vacancy_query(query_id):
    return [i.to_dict() for i in db.session.get(Query, query_id).vacancies.all()]


def get_query():
    max_salary = querys.maximum_salary_for_querys().all()
    min_salary_from = querys.min_salary_for_querys(Vacancy.salary_from).all()
    min_salary_to = querys.min_salary_for_querys(Vacancy.salary_to).all()

    response = {i[3]: {'name': i[4], 'count': i[2], 'max': max(i[0] if i[0] else 0, i[1] if i[1] else 0)} for i in
                max_salary}

    for i in min_salary_from:
        response[i[1]]['min'] = i[0] if i[0] else 0

    for i in min_salary_to:
        response[i[1]]['min'] = min(response[i[1]]['min'], (i[0] if i[0] else 0))

    return response


def post_query(name: str):
    db.session.add(Query(name=name))
    # db.session.flush()
    db.session.commit()


def delete_query(query_id):
    db.session.delete(db.session.get(Query, query_id))
    # db.session.flush()
    db.session.commit()


def get_aggregators():
    return [{'id': i.id, 'class_name': i.class_name, 'url': i.url}for i in Aggregator.query.all()]


def post_aggregator(name: str, class_name: str, url: str):
    db.session.add(Aggregator(id=name, class_name='class_name', url=url))
    # db.session.flush()
    db.session.commit()


def delete_aggregator(query_id):
    db.session.delete(db.session.get(Aggregator, query_id))
    # db.session.flush()
    db.session.commit()


def update_statistics():
    Statistics.query.delete()
    TopVacancies.query.delete()
    TopSkills.query.delete()

    db.session.add(Statistics(id=1, value_int=Vacancy.query.count()))
    db.session.add(Statistics(id=2, value_int=Skills.query.count()))

    for i in querys.top_vacancies(app.config['COUNT_TOP_VACANCIES']).all():
        db.session.add(TopVacancies(id=i[0]))

    for i in querys.top_skills(app.config['COUNT_TOP_SKILLS']).all():
        db.session.add(TopSkills(id=i[4], name=i[3], salary_max=i[1], salary_min=i[0]))

    db.session.commit()


def index_data():
    return {
        'count_vacancies': Statistics.query.get(1).value_int,
        'count_skills': Statistics.query.get(2).value_int,
        'top_vacancies': [Vacancy.query.get(i.id).to_dict() for i in TopVacancies.query.all()],
        'top_skills':  [{'min': i.salary_min, 'max': i.salary_max, 'name': i.name, 'id': i.id} for i in TopSkills.query.all()]
    }
