from datetime import datetime, timedelta
from pathlib import Path
import requests
from my_api.models import Vacancy, Skills, SkillsVacancy, Query
from my_api import db, app


def exists_and_makedir(path: str):
    Path(path).mkdir(parents=True, exist_ok=True)


def get_json_data(params: dict = None, header: dict = None, uri: str = None):
    if not header:
        header = app.config['HEADER']

    url = (app.config['BASE_URI'] + f'/{uri}/') if uri else app.config['BASE_URI']

    return requests.get(url=url, params=params, headers=header).json()


def get_all_vacancies(page=0, per_page=10, tag_id=None, query_id=None):

    if query_id:
        query = db.session.query(Vacancy).join(Vacancy.querys).filter(Query.id == query_id)
    else:
        query = Vacancy.query

    if tag_id:
        query = query.join(SkillsVacancy).join(Skills, SkillsVacancy.skill_id == Skills.id).filter(Skills.id == tag_id)

    return query.count(), query.offset(page * per_page).limit(per_page).all()


def get_vacancy_by_id(vacancy_id):
    return db.session.get(Vacancy, vacancy_id)


def get_vacancy_skills(vacancy_id):
    vacancy = db.session.get(Vacancy, vacancy_id)
    if not vacancy:
        return []
    return [skill.to_dict() for skill in vacancy.skill_vacancies]


def get_skill_vacancies(skill_id):
    skills_query = Skills.query

    count = skills_query.count()

    return [i.vacancy.to_dict() for i in Skills.query.get(skill_id).skill_vacancies]


def get_all_skills(page=0, per_page=10):
    skills_query = Skills.query.join(Skills.skill_vacancies).group_by(Skills.id)
    skills_query = skills_query.order_by(db.func.count(SkillsVacancy.skill_id).desc())

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
    return [{'id': i.id, 'name': i.name} for i in Query.query.all()]


def post_query(name: str):
    db.session.add(Query(name=name))
    # db.session.flush()
    db.session.commit()


def delete_query(query_id):
    db.session.delete(db.session.get(Query, query_id))
    # db.session.flush()
    db.session.commit()
