from datetime import datetime, timedelta
from pathlib import Path
import requests
from sqlalchemy import func, INT, desc
from my_api.models import Vacancy, Skills, Query
from my_api import db, app


def exists_and_makedir(path: str):
    Path(path).mkdir(parents=True, exist_ok=True)


def get_json_data(params: dict = None, header: dict = None, uri: str = None):
    if not header:
        header = app.config['HEADER']

    url = (app.config['BASE_URI'] + f'/{uri}/') if uri else app.config['BASE_URI']

    return requests.get(url=url, params=params, headers=header).json()


def get_all_vacancies(page=None, per_page=10):
    query = Vacancy.query

    count = query.count()

    if page is not None:
        query = query.offset(page * per_page).limit(per_page)

    return count, query.all()


def get_vacancy_by_id(vacancy_id):
    return db.session.get(Vacancy, vacancy_id)


def get_vacancy_skills(vacancy_id):
    return [skill.to_dict() for skill in db.session.get(Vacancy, vacancy_id).skills]


def get_skill_vacancies(skill_name):
    return [i.vacancy.to_dict() for i in Skills.query.filter(Skills.name == skill_name)]


def get_all_skills(page=None, per_page=10):
    skills_query = db.session.query(Skills.name,
                                    func.sum(func.cast(Skills.key_skill, INT)),
                                    func.sum(func.cast(Skills.description_skill, INT)),
                                    func.sum(func.cast(Skills.basic_skill, INT)),
                                    func.count(Skills.id).label('count_id')
                                    ).group_by(Skills.name).order_by(desc('count_id'))

    skills_query = skills_query.offset(page * per_page).limit(per_page).all()

    skills = [{'skill': i[0], 'key': i[1], 'description': i[2], 'basic': i[3], 'vacancies': i[4]} for i in skills_query]

    return skills


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
    return [{'id': i.id, 'name': i.name}for i in Query.query.all()]


def post_query(name: str):
    db.session.add(Query(name=name))
    # db.session.flush()
    db.session.commit()


def delete_query(query_id):
    db.session.delete(db.session.get(Query, query_id))
    # db.session.flush()
    db.session.commit()
